from django.shortcuts import render, redirect
from django.views import View
from .form import UserRegisterationForm, UserLoinForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages


class UserRegisterView(View):

    form_class = UserRegisterationForm
    temmplate_name = 'account/register.html'
    def get(self, request):
        form = self.form_class()
        return render(request, self.temmplate_name, {'form' : form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            
            User.objects.create_user(cd['username'], cd['email'], cd['password'])
            messages.success(request, 'succes register!', 'succes')

            return redirect('home:home')
        return render(request, self.temmplate_name, {'form' : form})


class UserLoginView(View):
    form_class = UserLoinForm
    template_name = 'account/login.html'
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form' : form})



    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'], password= cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'succes login!', 'succes')
                return redirect('home:home')
            messages.error(request, 'password is wrong', 'warning')
            
        return render(request, self.template_name, {'form': form})
