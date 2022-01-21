from django import forms
from django.contrib.auth import models
from django.forms.widgets import EmailInput, FileInput, PasswordInput, Textarea
from django.contrib.auth.models import User
from .models import UserProfile

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30,label="نام کاربری", widget=forms.TextInput(
        attrs={'class': 'login-input', 'placeholder' : 'نام کاربری'}))
    password = forms.CharField(max_length=50, label="رمز عبور",widget=PasswordInput(
        attrs={'class': 'login-input', 'placeholder' : 'رمز عبور'}))
    
class UserRegisterForm(forms.Form):
    username = forms.CharField(required=True,label="نام کاربری",max_length=30, widget=forms.TextInput(attrs={'class': 'login-input', 'placeholder' : 'نام کاربری'}))
    password = forms.CharField(required=True,label="رمز عبور",max_length=50,min_length=8, widget=PasswordInput(
        attrs={'class': 'login-input', 'placeholder' : 'رمز عبور'}))
    password2 = forms.CharField(label='تایید رمز عبور',min_length=8,required=True,max_length=50, widget=PasswordInput(
        attrs={'class': 'login-input', 'placeholder' : 'تکرار رمز عبور'}))
    email = forms.EmailField(max_length=50,label="ایمیل", widget=EmailInput(
        attrs={'class': 'login-input', 'placeholder' : 'ایمیل'}))

    def clean(self) :
        clean_data = super().clean()

        if 'email' in clean_data:
         email = clean_data['email']
         user = User.objects.filter(email = email)
         if user.exists():
             raise forms.ValidationError("با ایمیل وارد شده قبلا ثبت نام صورت گرفته شده لطفا ایمیل دیگری را انتخاب کنید")
       
      
        if 'username' in clean_data:
            username=clean_data['username']
            user = User.objects.filter(username=username)
            if user.exists():
             raise forms.ValidationError("بانام کاربری وارد شده قبلا ثبت نام صورت گرفته شده لطفا یوزرنیم دیگری را انتخاب کنید")
        

        if 'password' in clean_data and 'password2' in clean_data:
            password = clean_data['password']
            password2 = clean_data['password2']
            if password2 != password:
                 raise forms.ValidationError('رمز ها یکسان نیستند')

class ProfileEditForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = UserProfile
        fields = ("description",)