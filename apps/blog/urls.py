from django.contrib import admin
from django.urls import path
from apps.blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('articles/<int:id>/', views.detail, name='detail'),
]