from django.urls import path
from .views import *
from app import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    
    #path('base/<int:pk>/', views.base, name='base'),

    path('', views.index, name='index'),
    path('reg/', views.register, name='register'),
    path('accounts/login/', views.user_login, name='login'),

    path('profile/', views.user_profile, name='profile'),

    path('changepass/', views.user_change_pass, name='change_pass'),
    path('changepass1/', views.user_change_pass1, name='change_pass1'),


    path('logout/', views.user_logout, name='logout'),

    path('caty/', views.category, name='category'),
    
    path('productdetail/<int:pk>/', views.productdetail, name='productdetail'),

    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    #path('cart/', views.cart, name="cart"),

    path('plus-cart/<int:cart_id>/', views.plus_cart, name="plus-cart"),
    path('minus-cart/<int:cart_id>/', views.minus_cart, name="minus-cart"),
    path('remove-cart/<int:cart_id>/', views.remove_cart, name="remove-cart"),
    path('cartcheckout/', views.cart, name="cart"),


    path('orders/', views.orders, name="orders"),
    path('about-us/',views.about_us),

    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

