from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import contacts, ProductListView, ProductDetailView, ProductCreateView, ProductVersionUpdateView, \
    ProductDeleteView, CategoryListView, CategoryProductListView
from catalog.views import custom_permission_denied

app_name = CatalogConfig.name

urlpatterns = [
    path('contacts/', contacts, name='contacts'),
    path('', ProductListView.as_view(), name='index'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('category/<int:category_id>/products/', CategoryProductListView.as_view(), name='category_products'),
    path('product/<int:pk>', cache_page(60)(ProductDetailView.as_view()), name='product'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>', ProductVersionUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>', ProductDeleteView.as_view(), name='product_delete'),
    path('permission-denied/', custom_permission_denied, name='permission_denied'),
]
