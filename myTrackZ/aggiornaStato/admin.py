from django.contrib import admin
from .models import Cliente, Ordine, Prodotto
# Register your models here.


admin.site.register(Cliente)
admin.site.register(Ordine)
admin.site.register(Prodotto)