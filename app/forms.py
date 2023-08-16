from django import forms
from django.contrib.auth.models import User
from app.models import *

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['total_amount']  # Add any additional fields if needed

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']
