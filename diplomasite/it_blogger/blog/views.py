from django.shortcuts import render
from django.views.generic import ListView, DetailView

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
        context['cat_selected'] = 0
        context['menu'] = menu
        return context

    def get_queryset(self):
        return Blog.objects.filter(is_published=True).select_related("category")


class ShowPost(DetailView):
    model = Blog
    template_name = "blog/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context


class BlogCategory(ListView):
    model = Blog
    template_name = "blog/post.html"
    context_object_name = 'posts'

    def get_queryset(self):
        return Blog.objects.filter(category__slug=self.kwargs["category_slug"], is_published=True).select_related(
            "category")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Категория - " + str(context['posts'][0].category)
        context['cat_selected'] = context['posts'][0].category_id
        context['menu'] = menu
        return context
