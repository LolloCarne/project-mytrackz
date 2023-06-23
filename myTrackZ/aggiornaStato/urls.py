from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('', views.prova),
   path('getInfo/',views.getInfo),
]