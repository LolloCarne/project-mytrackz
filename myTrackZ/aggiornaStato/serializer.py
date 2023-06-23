from rest_framework import serializers
from .models import Prodotto,Ordine
class ProdottoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Prodotto
        fields= '__all__'

class OrdineSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ordine
        fields='__all__'