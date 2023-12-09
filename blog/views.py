from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from blog.models import Blogpost


# Create your views here.

class BlogpostCreateView(CreateView):
    model = Blogpost
    fields = ('title', 'content',)
    success_url = reverse_lazy('blog:list')


class BlogpostListView(ListView):
    model = Blogpost


class BlogpostDetailView(DetailView):
    model = Blogpost


class BlogpostUpdateView(UpdateView):
    model = Blogpost
    fields = ('title', 'content',)
    success_url = reverse_lazy('blog:list')
