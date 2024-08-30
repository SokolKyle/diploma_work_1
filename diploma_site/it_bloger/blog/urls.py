from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from .views import *

urlpatterns = [
    path('', BlogHome.as_view(), name='index'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', BlogCategory.as_view(), name='category'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('post/<slug:post_slug>/rate/', RatePost.as_view(), name='rate_post'),
    path('post/<slug:post_slug>/comment/', CommentPost.as_view(), name='comment_post'),
    path('accounts/login/', LoginUser.as_view(), name='login'),
    path('unauthenticated_redirect/', TemplateView.as_view(template_name='blog/unauthenticated_redirect.html'),
         name='unauthenticated_redirect'),
    path('info/', TemplateView.as_view(template_name='blog/info.html'), name='info'),
]
