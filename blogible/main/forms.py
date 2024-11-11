from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=20, min_length=5, widget=forms.TextInput(attrs={
        'class':'SM-text-field',
        'placeholder':'Username',
    }))
    password = forms.CharField(min_length=3, max_length=20, widget=forms.PasswordInput(attrs={
        'class':'SM-text-field',
        'placeholder':'Password',
    }))
    