from django.conf import settings
from django.db import models, connection
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

NULLABLE = {"null": True, "blank": True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование категории')
    description = models.TextField(verbose_name='описание категории')

    @classmethod
    def truncate_table_restart_id(cls):
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ("name",)


class Product(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='владелец', **NULLABLE)
    name = models.CharField(max_length=100, verbose_name='наименование продукта')
    description = models.TextField(verbose_name='описание продукта')
    image = models.ImageField(upload_to='products/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    price = models.IntegerField(verbose_name='цена')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')
    time_update = models.DateTimeField(auto_now=True, verbose_name='дата изменения')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ("name",)

    def can_edit(self, user):
        return self.owner == user


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    version_number = models.PositiveSmallIntegerField(verbose_name='номер версии')
    version_name = models.CharField(max_length=150, verbose_name='название версии', **NULLABLE)
    is_active = models.BooleanField(verbose_name='активная версия', **NULLABLE)

    # переопределяем сейв метод для установки единственной is_active версии (*)
    def save(self, *args, **kwargs):
        if self.is_active:
            Version.objects.filter(product=self.product).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.version_number} - {self.version_name}: {self.is_active}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
