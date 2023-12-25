import random
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy, reverse
from django.views import View
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
    success_url = reverse_lazy('users:verification_code')
    template_name = 'users/register.html'
    extra_context = {
        'title': 'Регистрация пользователя'
    }

    def form_valid(self, form):
        password = User.objects.make_random_password()
        new_user = form.save(commit=False)
        new_user.verification_code = password
        new_user.save()
        send_mail(
            recipient_list=[new_user.email],
            subject='Регистрация на сайте Skystore',
            message=f'Введите код из для подтверждения регистрации: {new_user.verification_code}',
            from_email=settings.EMAIL_HOST_USER,
        )
        return super().form_valid(form)


class VerificationCodeView(View):
    model = User
    template_name = 'users/verification_code.html'

    def get(self, request):
        return render(request, self.template_name)

    @staticmethod
    def post(request):
        verification_code = request.POST.get('verification_code')
        user = User.objects.filter(verification_code=verification_code).first()

        if user is not None and user.verification_code == verification_code:
            user.save()
            return redirect(reverse('users:login'))


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')
    extra_context = {
        'title': 'Редактирование профиля'
    }

    def get_object(self, queryset=None):
        return self.request.user


def new_password_generate(request):
    # new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    new_password = User.objects.make_random_password()

    send_mail(
        subject='Смена пароля вашего аккаунта',
        message=f'Ваш пароль изменен успешно на: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )

    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('catalog:index'))
