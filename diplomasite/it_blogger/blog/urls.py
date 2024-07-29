from django.urls import path

from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='index'),
    path('blogs/', BlogHome.as_view(), name='blogs'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:category_slug>/', BlogCategory.as_view(), name='category'),
]
