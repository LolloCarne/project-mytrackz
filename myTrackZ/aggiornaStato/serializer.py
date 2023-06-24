from rest_framework import serializers
from .models import Prodotto,Ordine,Cliente
class ProdottoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Prodotto
        fields= '__all__'

class OrdineSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ordine
        fields='__all__'


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cliente
        fields='__all__'