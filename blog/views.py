from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from blog.models import Blogpost


# Create your views here.

class BlogpostCreateView(CreateView):
    model = Blogpost
    fields = ('title', 'content', 'date_create',)
    success_url = reverse_lazy('blog:list')


class BlogpostListView(ListView):
    model = Blogpost


class BlogpostDetailView(DetailView):
    model = Blogpost

