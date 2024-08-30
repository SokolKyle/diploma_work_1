from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, FormView, View, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *

from .utils import *


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'blog/contact.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        subject = "Message"
        body = {
            'name': form.cleaned_data['name'],
            'email': form.cleaned_data['email'],
            'content': form.cleaned_data['content'],
        }
        message = "\n".join(body.values())
        try:
            send_mail(
                subject, message,
                form.cleaned_data['email'],
                ['sokoloffKyle@mail.ru']
            )
        except BadHeaderError:
            return HttpResponse('Найден не корректный заголовок')
        return redirect('index')


class BlogHome(DataMixin, ListView):
    model = Blog
    template_name = "blog/index.html"
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Blog.objects.filter(is_published=True).select_related("cat")


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = "blog/login.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "blog/register.html"
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class ShowPost(DataMixin, DetailView):
    model = Blog
    template_name = "blog/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        context['ratings'] = self.get_ratings(context['post'])
        context['comments'] = context['post'].comments.all()
        context['comment_form'] = CommentForm()
        return dict(list(context.items()) + list(c_def.items()))

    def get_ratings(self, post):
        helpful_count = post.ratings.filter(helpful=True).count()
        not_helpful_count = post.ratings.filter(helpful=False).count()
        return {
            'helpful_count': helpful_count,
            'not_helpful_count': not_helpful_count
        }


class RatePost(View):
    def post(self, request, post_slug):
        if not request.user.is_authenticated:
            return redirect('unauthenticated_redirect')

        post = get_object_or_404(Blog, slug=post_slug)
        helpful = request.POST.get('helpful') == 'true'
        Rating.objects.update_or_create(blog=post, user=request.user, defaults={'helpful': helpful})
        return redirect(post.get_absolute_url())


class CommentPost(View):
    def post(self, request, post_slug):
        if not request.user.is_authenticated:
            return redirect('unauthenticated_redirect')

        post = get_object_or_404(Blog, slug=post_slug)
        content = request.POST.get('content')
        parent_comment_id = request.POST.get('parent_comment_id')

        if parent_comment_id:
            parent_comment = get_object_or_404(Comment, id=parent_comment_id)
            comment = Comment.objects.create(blog=post, user=request.user, content=content, parent=parent_comment)
        else:
            comment = Comment.objects.create(blog=post, user=request.user, content=content)

        return redirect(post.get_absolute_url())


class BlogCategory(DataMixin, ListView):
    model = Blog
    template_name = "blog/index.html"
    context_object_name = 'posts'

    def get_queryset(self):
        return Blog.objects.filter(cat__slug=self.kwargs["cat_slug"], is_published=True).select_related("cat")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title="Категория - " + str(c.name), cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "blog/addpage.html"
    success_url = reverse_lazy("index")
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))
