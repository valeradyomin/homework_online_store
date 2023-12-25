from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, ProductListView, ProductDetailView, ProductCreateView, ProductVersionUpdateView, \
    ProductDeleteView
from catalog.views import custom_permission_denied

app_name = CatalogConfig.name

urlpatterns = [
    # path('', index, name='index'),  # FBV
    path('contacts/', contacts, name='contacts'),  # FBV
    # path('product/<int:pk>', product, name='product'),  # FBV
    path('', ProductListView.as_view(), name='index'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>', ProductVersionUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>', ProductDeleteView.as_view(), name='product_delete'),
    path('permission-denied/', custom_permission_denied, name='permission_denied'),
]
