from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version


# Create your views here.

class ProductListView(ListView):
    model = Product
    # template_name = 'catalog/product_list.html'
    extra_context = {
        'title': 'Товары нашего магазина'
    }

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        products = Product.objects.all()
        active_versions = Version.objects.filter(is_active=True, product__in=products)
        context_data['active_versions'] = active_versions
        return context_data


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

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        products = Product.objects.all()
        active_versions = Version.objects.filter(is_active=True, product__in=products)
        context_data['active_versions'] = active_versions
        return context_data


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
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')

    extra_context = {
        'title': 'Добавление товара'
    }

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ProductVersionUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    extra_context = {
        'title': 'Изменение товара'
    }

    def get_success_url(self):
        return reverse('catalog:index')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)
