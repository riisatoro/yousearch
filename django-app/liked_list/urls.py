from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.Main.as_view()),
    path('add/', views.NewLiked.as_view()),
]
