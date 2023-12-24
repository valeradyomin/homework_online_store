from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, LoginViewForm, UserForm
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

    def form_valid(self, form):
        new_user = form.save()
        send_mail(
            subject='Поздравляем с регистрацией на сайте Skystore!',
            message='Вы успешно зарегистрировались на нашей платформе.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')
    extra_context = {
        'title': 'Редактирование профиля'
    }

    def get_object(self, queryset=None):
        return self.request.user
