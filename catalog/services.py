from django.core.cache import cache

from catalog.models import Category
from config.settings import CACHE_ENABLED


def get_cache_categories():
    if CACHE_ENABLED:
        # Проверяем включенность кеша
        key = 'categories'  # Создаем ключ для хранения
        categories = cache.get(key)  # Пытаемся получить данные
        if categories is None:
            # Если данные не были получены из кеша, то выбираем из БД и записываем в кеш
            categories = Category.objects.all()
            cache.set(key, categories)
    else:
        # Если кеш не был подключен, то просто обращаемся к БД
        categories = Category.objects.all()
    # Возвращаем результат
    return categories
