from django import forms
from django.contrib.auth.models import User

from .models import Profile

class LoginForm(forms.Form):
    '''登录表单类'''
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    '''用户注册表单类'''
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)
   
    class Meta:
        model = User
        fields = ('username','first_name','email')
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match!')
        return cd['password2']

class UserEditForm(forms.ModelForm):
    '''这是修改基本信息的表单类'''
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class ProfileEditForm(forms.ModelForm):
    '''这是修改附加信息的表单类'''
    class Meta:
        model = Profile
        fields = ['date_of_birth','photo']