from django import forms
from .models import *

class RegisterationForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ('username','first_name','last_name','email','password',)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ('username','first_name','last_name','email')

class OtpForm(forms.Form):
    otp = forms.CharField(max_length=4)

class LoginForm(forms.Form):
        username = forms.CharField(max_length=100)
        password = forms.CharField(max_length=100,widget=forms.PasswordInput)
