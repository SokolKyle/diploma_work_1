from django.urls import path

from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='index'),
    path('blogs/', BlogHome.as_view(), name='blogs'),
]
