from django.contrib import admin

from users.models import User


# Register your models here.

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'country', 'avatar',)
    # verbose_name = 'Пользователи'
