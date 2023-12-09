from django.db import models

# Create your models here.
NULLABLE = {"null": True, "blank": True}


class Blogpost(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(unique=True, max_length=300, verbose_name='slug')
    content = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='blogpost/', verbose_name='изображение', **NULLABLE)

