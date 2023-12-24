from django.shortcuts import render
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView

from users.models import User


# Create your views here.


class LoginView(BaseLoginView):
    model = User
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Вход пользователя'
    }


class LogoutView(BaseLogoutView):
    pass
