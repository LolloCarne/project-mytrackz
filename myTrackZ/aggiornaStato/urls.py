from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('', views.prova,name="prova"),
   path('getInfo/',views.getInfo),
   path('createUser/',views.createUser),
   path('aggiorna/',views.aggiorna),
]