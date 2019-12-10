from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homepage),
    path('create/', views.create),
    path('sobre/', views.sobre),
    path('resultado/', views.resultado_detail)
]
