from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from catalog.models import Product


# Create your views here.

class ProductListView(ListView):
    model = Product
    # template_name = 'catalog/product_list.html'
    extra_context = {
        'title': 'Товары нашего магазина'
    }


# def index(request):
#     context = {
#         'object_list': Product.objects.all(),
#         'title': 'Товары нашего магазина'
#     }
#     return render(request, 'catalog/product_list.html', context=context)


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


class ProductDetailView(DetailView):
    model = Product
    # template_name = 'catalog/product_detail.html'
    extra_context = {
        'title': 'Обзор товара'
    }


# def product(request, pk):
#     product_item = Product.objects.get(id=pk)
#
#     context = {
#         'object': product_item,
#         'title': f'Товар - {product_item.name}'
#     }
#     return render(request, 'catalog/product_detail.html', context=context)


class ProductCreateView(CreateView):
    model = Product
