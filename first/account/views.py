from django.shortcuts import render, redirect
from django.views import View
from .form import UserRegisterationForm
from django.contrib.auth.models import User
from django.contrib import messages


class RegisterView(View):

    form_class = UserRegisterationForm()
    temmplate_name = 'account/register.html'
    def get(self, request):
        form = self.form_class
        return render(request, self.temmplate_name, {'form' : form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if User.objects.filter(username=cd['username']).exists():
                messages.error(request, "این نام کاربری قبلاً ثبت شده")
                return redirect('register:user_register')

            if User.objects.filter(email=cd['email']).exists():
                messages.error(request, "این ایمیل قبلاً ثبت شده")
                return redirect('register:user_register')
            
            User.objects.create_user(cd['username'], cd['email'], cd['password'])
            messages.success(request, 'succes register!', 'succes')

            return redirect('home:home')
        return render(request, self.temmplate_name, {'form' : form})
