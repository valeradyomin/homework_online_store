from django.shortcuts import render
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserRegisterForm, LoginViewForm
from users.models import User


# Create your views here.


class LoginView(BaseLoginView):
    model = User
    form_class = LoginViewForm
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Вход пользователя'
    }


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'
    extra_context = {
        'title': 'Регистрация пользователя'
    }

