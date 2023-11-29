import datetime

from django.db import models

NULLABLE = {"null": True, "blank": True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование категории')
    description = models.TextField(verbose_name='описание категории')
    created_at = models.DateTimeField(verbose_name='дата создания', default=datetime.datetime.now)

    def __str__(self):
        return f'{self.name} - {self.description}'

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ("name",)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование продукта')
    description = models.TextField(verbose_name='описание продукта')
    image = models.ImageField(upload_to='products/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    price = models.IntegerField(verbose_name='цена')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')
    time_update = models.DateTimeField(auto_now=True, verbose_name='дата изменения')

    def __str__(self):
        return f'{self.category}:{self.name}({self.price}) - {self.description}'

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ("name",)
