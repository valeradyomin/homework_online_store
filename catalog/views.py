from django.shortcuts import render

from catalog.models import Product


# Create your views here.

def index(request):
    context = {
        'object_list': Product.objects.all(),
        'title': 'Товары нашего магазина'
    }
    return render(request, 'catalog/index.html', context=context)


def contacts(request):
    context = {
        'title': 'Наши контакты'
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Пользователь {name} ( номер телефона: {phone}) оставил сообщение: {message}')
    return render(request, 'catalog/contacts.html', context=context)


def product(request, pk):
    product_item = Product.objects.get(id=pk)

    context = {
        'object': product_item,
        'title': f'Товар - {product_item.name}'
    }
    return render(request, 'catalog/product.html', context=context)
