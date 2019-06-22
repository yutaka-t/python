# -*- coding:utf-8 -*-

from django.urls import path, include
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>', views.post_detail, name="post_detail")
]
