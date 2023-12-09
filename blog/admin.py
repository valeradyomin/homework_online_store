from django.contrib import admin

from blog.models import Blogpost


@admin.register(Blogpost)
class AdminBlogpost(admin.ModelAdmin):
    list_display = ('title', 'content', 'is_published',)
