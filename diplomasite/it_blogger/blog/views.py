from django.shortcuts import render
from django.views.generic import ListView

from .models import *

menu = [
    {'title': 'Статьи', 'url_name': 'blogs'},
    {'title': 'Добавить статью', 'url_name': 'index'},
    {'title': 'войти', 'url_name': 'index'},
]


class HomePage(ListView):
    model = HomePage
    template_name = "blog/index.html"
    context_object_name = 'home'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Coder'sCorner "
        context['menu'] = menu
        return context


class BlogHome(ListView):
    model = Blog
    template_name = "blog/blogs.html"
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Статьи"
        context['menu'] = menu
        return context
