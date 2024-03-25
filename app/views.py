import decimal
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from .forms import*
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator # for Class Based Views
from django.views import View
# import requests
from django.urls import reverse

from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from .mongo_connect import my_client

def about_us(request):
    return render(request,template_name='app/about_us.html')

# Create your views here.

def index(request):
    cat = Category.objects.all()
    return render(request, 'app/category.html',  {'category':cat})


def category(request):
    cat = Category.objects.all()
    return render(request, 'app/category.html',  {'category':cat})



def productdetail(request, pk):
    product = Product.objects.get(id=pk)
            
    return render(request, 'app/productdetail.html', {
        'product': product,
    })

    

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    # Check whether the Product is alread in Cart or Not
    item_already_in_cart = Cart.objects.filter(product=product_id, user=user)
    if item_already_in_cart:
        cp = get_object_or_404(Cart, product=product_id, user=user)
        cp.quantity += 1
        cp.save()
    else:
        Cart(user=user, product=product).save()

    return redirect('cart')
import datetime
@login_required
def cart(request):
    user = request.user
    cart_products = Cart.objects.filter(user=user)
    cp = [p for p in Cart.objects.all() if p.user==user]
    amount = decimal.Decimal(0)
    total_amount=0
    shipping = 100
    if cp:
        for p in cp:
            temp_amount = (p.quantity*p.product.price)
            amount += temp_amount
            
            total_amount = amount + shipping

    if request.method == 'POST':
        fm = CheckoutForm(request.POST)
        user = request.user
        if fm.is_valid():
            cart = Cart.objects.filter(user=user)
            address = fm.cleaned_data['address']
            mobile = fm.cleaned_data['mobile']
            pm = fm.cleaned_data['payment_method']
            order_lists = []
            for c in cart:
                image_url = ''
                if c.product.product_image.url:
                    image_url = c.product.product_image.url
                order = {
                    'user':c.user.username,
                    'product':c.product.name,
                    'address':address,
                    'mobile':mobile,
                    'quantity':c.quantity,
                    'total_amount':float(total_amount),
                    'payment_method':pm,
                    'status':'pending',
                    'image_url':image_url,
                    'ordered_date':datetime.datetime.now(tz=datetime.timezone.utc)

                }
                order_lists.append(order)
                
                print("order===",order)


                    
                # And Deleting from Cart
                c.delete()
            dbname = my_client['sweetstore']
            collection_name = dbname["orders"]
            collection_name.insert_many(order_lists)
            return redirect('cart')

    else:
        fm = CheckoutForm()

    context = {
        'cart_products': cart_products,
        'amount':amount,
        'total_amount':total_amount ,
        'shipping':shipping,
        'form':fm

       }

    return render(request, 'app/cart_checkout.html', context)


@login_required
def remove_cart(request, cart_id):
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        
    return redirect('cart')


@login_required
def plus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        cp.save()
    return redirect('cart')


@login_required
def minus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        # Remove the Product if the quantity is already 1
        if cp.quantity == 1:
            cp.delete()
        else:
            cp.quantity -= 1
            cp.save()
    return redirect('cart')

@login_required
def checkout(request):
    user = request.user
    address_id = request.get('address')
    address = get_object_or_404(Address, id=address_id)    
    payment = request.get('payment')
    
    # Get all the products of User in Cart
    cart = Cart.objects.filter(user=user)
    for c in cart:
        # Saving all the products from Cart to Order
        Ordered(user=user, address=address, product=c.product, quantity=c.quantity,payment_method=payment).save()
        c.delete()
     
        # And Deleting from Cart
        
    return redirect('cart')

@login_required
def orders(request):
    dbname = my_client['sweetstore']
    collection_name = dbname["orders"]
    results = collection_name.find({'user':request.user.username})
    orders = []
    for document in results:
        # pprint.pprint(document)
        orders.append(document)
    print("orders==",orders)
    
    return render(request, 'app/orders.html', {'orders': orders})


def base(request):
    return render(request, 'app/newbase.html')

def register(request):

    if request.method == 'POST':
        fm = CustomerRegistrationForm(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, 'Registration successful!')

            fm = CustomerRegistrationForm()

    else:
        fm = CustomerRegistrationForm()
    

    return render(request, 'app/register.html', {'form':fm})

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/profile/')
    if request.method == 'POST':
        fm = AuthenticationForm(data=request.POST)
        if fm.is_valid():
            user = fm.get_user()
            login(request, user)
            message = f'Welcome {request.user.username}'
            messages.success(request,message)
            return HttpResponseRedirect('/profile/')

    else:
        fm = AuthenticationForm()
    return render(request, 'app/user_login.html',{'form':fm})




def user_profile(request):
    if request.user.is_authenticated:
        #address = Address.objects.all()
        #address = Address.objects.filter(user=request.user)
        if request.method == 'POST':
            fm = EditUserProfileForm(request.POST, instance=request.user)
            if fm.is_valid():
                messages.success(request, 'Profile Updated !!')
                fm.save()
        else:
            fm = EditUserProfileForm( instance=request.user)
        return render(request, 'app/profile.html', {'name': request.user, 'fm':fm})
    else:
        return HttpResponseRedirect('/login/')


#Change Password with old password
def user_change_pass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request, 'Password change sucessfully !!')
                return redirect('profile')
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request, 'app/change_password.html', {'fm':fm})
    else:
        return HttpResponseRedirect('/accounts/login/')


#Change Password without old password
def user_change_pass1(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = SetPasswordForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request, 'Password change sucessfully !!')
                return redirect('profile')
        else:
            fm = SetPasswordForm(user=request.user)
        return render(request, 'app/change_password.html', {'fm':fm})
    else:
        return HttpResponseRedirect('/accounts/login/')


def user_logout(request):
    logout (request)
    return HttpResponseRedirect('/accounts/login/')
