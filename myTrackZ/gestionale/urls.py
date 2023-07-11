from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('addUtente/',views.addUtente),
   path('addOrdine/',views.addOrdine),
   path('addProdotto/',views.addProdotto),
   path('getOrdini/',views.getOrdini),
   path('getProdotti/',views.getProdotti),
   path('getClienti/',views.getClienti),
   path('signup/',views.signup),
   path('login/',views.login)
]