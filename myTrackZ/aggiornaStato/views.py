from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Prodotto
from .serializer import OrdineSerializer,ProdottoSerializer
# Create your views here.

def prova(request):
    return render(request,'aggiornaStato/prova.html')


@api_view(['GET'])
def getInfo(request):
    item=Prodotto.objects.filter(prodottoId=request.headers['id'])
    serializer=ProdottoSerializer(item)
    return Response(serializer.data)