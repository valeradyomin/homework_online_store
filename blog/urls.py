from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogpostCreateView, BlogpostListView

app_name = BlogConfig.name

urlpatterns = [
    path('create', BlogpostCreateView.as_view(), name='create'),
    path('', BlogpostListView.as_view(), name='list'),
    # path('view/<int:pk>/', ..., name='view'),
    # path('edit/<int:pk>/', ..., name='edit'),
    # path('delete/<int:pk>/', ..., name='delete'),
]
