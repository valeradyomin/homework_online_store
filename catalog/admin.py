from django.contrib import admin

from catalog.models import Product, Category, Version


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Version)
class AdminVersion(admin.ModelAdmin):
    list_display = ('product', 'version_number', 'version_name', 'is_active',)
    list_filter = ('product', 'is_active',)
    search_fields = ('version_name',)
