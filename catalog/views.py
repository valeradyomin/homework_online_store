from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, ModeratorForm
from catalog.models import Product, Version

from django.shortcuts import get_object_or_404


# Create your views here.

class MyLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        return redirect(reverse('catalog:permission_denied'))


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    login_url = 'users:login'
    # template_name = 'catalog/product_list.html'
    extra_context = {
        'title': 'Товары нашего магазина'
    }

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Product.objects.all()
        else:
            return Product.objects.filter(is_published=True)

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


class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Product
    # template_name = 'catalog/product_detail.html'
    extra_context = {
        'title': 'Обзор товара'
    }
    permission_required = 'catalog.view_product'

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

class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')
    login_url = 'users:login'

    permission_required = 'catalog.add_product'

    extra_context = {
        'title': 'Добавление товара'
    }

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ProductVersionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    # form_class = ProductForm
    login_url = 'users:login'
    permission_required = 'catalog.change_product'

    extra_context = {
        'title': 'Изменение товара'
    }

    def get_form_class(self):
        if self.request.user.is_staff:
            return ModeratorForm
        else:
            return ProductForm

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

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     if not self.object.can_edit(request.user):
    #         return custom_permission_denied(request, pk=self.object.pk)
    #     return super().get(request, *args, **kwargs)
    #
    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     if not self.object.can_edit(request.user):
    #         return custom_permission_denied(request, pk=self.object.pk)
    #     return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


def custom_permission_denied(request, pk=None):
    owner_email = "нет владельца"
    if pk:
        product = get_object_or_404(Product, pk=pk)
        owner_email = product.owner.email if product.owner else "нет владельца"
    context = {
        'title': 'Упс... что то пошло не так',
        'reason': 'Вы не зарегистрированы либо не являетесь владельцем этого товара.',
        'owner_email': owner_email
    }
    return render(request, 'catalog/permission_denied.html', context=context)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')
    extra_context = {
        'title': 'Удаление товара',
    }

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     if not self.object.can_edit(request.user):
    #         return custom_permission_denied(request, pk=self.object.pk)
    #     return super().get(request, *args, **kwargs)
