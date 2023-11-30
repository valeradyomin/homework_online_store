import json
from django.core.management import BaseCommand
from catalog.models import Category, Product

db_json = 'catalog_data.json'


class Command(BaseCommand):
    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()
        with open(db_json, encoding='utf-8') as file:
            data = json.load(file)
            categories_to_create = []
            products_to_create = []
            for item in data:
                model = item['model']
                pk = item['pk']
                fields = item['fields']
                if model == 'catalog.category':
                    category = Category(id=pk, **fields)
                    categories_to_create.append(category)
                elif model == 'catalog.product':
                    category_id = fields.pop('category')
                    fields['category_id'] = category_id
                    product = Product(id=pk, **fields)
                    products_to_create.append(product)
            Category.objects.bulk_create(categories_to_create)
            Product.objects.bulk_create(products_to_create)
