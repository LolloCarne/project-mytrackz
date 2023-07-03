from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('addUtente/',views.addUtente),
   path('addOrdine/',views.addOrdine),
   path('addProdotto/',views.addProdotto),
   path('getOrdini/',views.getOrdini),
]