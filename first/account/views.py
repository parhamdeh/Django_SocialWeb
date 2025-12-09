from django.shortcuts import render, redirect
from django.views import View
from .form import UserRegisterationForm, UserLoinForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import Realation

class UserRegisterView(View):

    form_class = UserRegisterationForm
    temmplate_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
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

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
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
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request, 'password is wrong', 'warning')
            
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return redirect('home:home')
    #     return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        logout(request)
        messages.success(request, 'you loged out succesfuly!', 'success')
        return redirect('home:home')

class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        is_following = False
        user = User.objects.get(pk=user_id)
        posts = user.posts.all()
        relation = Realation.objects.filter(from_user = request.user, to_user = user)
        if relation.exists():
            is_following = True

        return render(request, 'account/profile.html', {'user':user, 'posts':posts, 'is_following':is_following})
    
class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('register:password_reset_done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView, View):
    template_name = 'account/password_reset_done.html'

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView, View):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('register:password_reset_complete')

class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView, View):
    template_name = 'account/password_reset_complete.html'



class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        realation = Realation.objects.filter(from_user = request.user, to_user = user)
        if realation.exists():
            messages.error(request, 'you are already following this user!', 'danger')
        else:
            Realation(from_user = request.user, to_user=user).save()
            messages.success(request, f'you followed {user.username}', 'success')
        return redirect('register:user_profile', user.id)


class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        realation = Realation.objects.filter(from_user = request.user, to_user = user)
        if realation.exists():
            realation.delete()
            messages.success(request, f'you unfollowed {user.username}', 'success')
            
        else:
            
            messages.error(request, 'you are not following this user!', 'danger')
            
        return redirect('register:user_profile', user.id)