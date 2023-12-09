from django.db import models

# Create your models here.
NULLABLE = {"null": True, "blank": True}


class Blogpost(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(unique=True, max_length=100, verbose_name='slug', **NULLABLE)
    content = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='blogpost/', verbose_name='изображение', **NULLABLE)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return f'Публикация: {self.title}'

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = "публикации"
        ordering = ("-date_create",)
