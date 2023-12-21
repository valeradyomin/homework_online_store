from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, ProductListView, ProductDetailView, ProductCreateView, ProductVersionUpdateView

app_name = CatalogConfig.name

urlpatterns = [
    # path('', index, name='index'),  # FBV
    path('contacts/', contacts, name='contacts'),  # FBV
    # path('product/<int:pk>', product, name='product'),  # FBV
    path('', ProductListView.as_view(), name='index'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>', ProductVersionUpdateView.as_view(), name='product_update'),
]
