from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField,UserChangeForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User
#from django.forms import fields, widgets
#from django.utils.translation import gettext, gettext_lazy as _ 
#from django.contrib.auth import password_validation
from .models import *
#from app import models

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password(again)', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email':'Email'}
        widgets =  {'username':forms.TextInput(attrs={'class':'form-control'})}

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class': 'form-control'}))
    password = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class': 'form-control'}))

class CheckoutForm(forms.Form):
    address = forms.CharField(required=True,max_length=100)
    mobile = forms.IntegerField(widget=forms.NumberInput())
    payment_method = forms.ChoiceField(choices=[('Cash', 'Cash')], widget=forms.Select())
    

class EditUserProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'email']
        help_texts = {'username':('')}  