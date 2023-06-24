from django.shortcuts import render, redirect 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Prodotto
from .serializer import OrdineSerializer,ProdottoSerializer,ClienteSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse


from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def prova(request):
    return render(request,'aggiornaStato/prova.html')


@api_view(['GET'])
def getInfo(request):
    item=Prodotto.objects.get(prodottoId=request.headers['id'])
    serializer=ProdottoSerializer(item)
    return Response(serializer.data)

@api_view(['PUT'])
def aggiorna(request):
    if int(request.headers['stato'])>4:
        return Response({"error":"Stato inesitente"},status=status.HTTP_400_BAD_REQUEST)
    try:
        Prodotto.objects.filter(prodottoId=request.headers['id']).update(stato=request.headers['stato'])
        Prodotto.objects.get(prodottoId=request.headers['id']).save()
    except:
        return Response({"error":"Errore nell'update"},status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def createUser(request):
    serializer=ClienteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)



