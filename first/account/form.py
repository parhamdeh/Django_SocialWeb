from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegisterationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder':'your name: '}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class' : 'form-control', 'placeholder':'your email: '}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    password2 = forms.CharField(label='confrim password', widget=forms.PasswordInput(attrs={'class' : 'form-control'}))


    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email already exists!')
        return email
    

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('this username already exists!')
        return username
    
    def clean(self):
        cd = super().clean()
        password = cd.get('password')
        password2 = cd.get('password2')

        if password and password2 and password != password2:
            raise ValidationError('password must match')
        


class UserLoinForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder':'your name: '}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class' : 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            return username
        raise ValidationError('this username not exists!')
    
    