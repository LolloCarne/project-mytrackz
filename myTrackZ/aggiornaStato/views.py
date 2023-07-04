from django.shortcuts import render, redirect 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Prodotto, Ordine, Cliente
from .serializer import OrdineSerializer,ProdottoSerializer,ClienteSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
import uuid


from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def aggiornaStatoProdotto(stato,id):
        try:
            Prodotto.objects.filter(prodottoId=id).update(stato=stato)
            prodotto=Prodotto.objects.get(prodottoId=id)
            prodotto.save()
        except:
            return Response({"error":"Errore nell'update"},status=status.HTTP_400_BAD_REQUEST)

def prova(request):
    return render(request,'aggiornaStato/prova.html')


@api_view(['GET'])
def getInfo(request):
    item=Prodotto.objects.get(prodottoId=request.headers['id'])
    ordineId=Prodotto.objects.get(prodottoId=request.headers['id']).ordineId.ordineId
    ordine=Ordine.objects.get(ordineId=ordineId)
    clienteId=ordine.clienteId.clienteId
    cliente= Cliente.objects.get(clienteId=clienteId)

    serializerP=ProdottoSerializer(item)
    serializerO=OrdineSerializer(ordine)
    serializerC=ClienteSerializer(cliente)
    risposta={"Prodotto":serializerP.data,
              "Ordine": {"OrdineId":serializerO.data["ordineId"],"Stato":serializerO.data["flagStatoOrdine"]},
              "Cliente":{"email":serializerC.data["email"],"Azienda":serializerC.data["ragioneSociale"]}}
    return Response(risposta)

@api_view(['PUT'])
def aggiorna(request):

    if int(request.headers['stato'])>4:
        return Response({"error":"Stato inesitente"},status=status.HTTP_400_BAD_REQUEST)

    prodotto=Prodotto.objects.get(prodottoId=request.headers['id'])
    if  int(request.headers['stato']) < int(prodotto.stato):
        ordineid=prodotto.ordineId.ordineId
        ordine=Ordine.objects.get(ordineId=ordineid)
        if ordine.flagStatoOrdine:
            aggiornaStatoProdotto(request.headers['stato'],request.headers['id'])
            Ordine.objects.filter(ordineId=ordineid).update(flagStatoOrdine=False)
            return Response({"Avviso":"Stato retrocesso e ordine riaperto"},status=status.HTTP_200_OK)    
    aggiornaStatoProdotto(request.headers['stato'],request.headers['id'])
    if int(request.headers['stato'])==4:
        tempFlag=True
        ordine=prodotto.ordineId
        for p in Prodotto.objects.filter(ordineId=ordine).all():
            if int(p.stato) <4:
                tempFlag=False
                return Response({"Avviso":"Ordine non completato"},status=status.HTTP_200_OK)
        
        if tempFlag==True:
            id=prodotto.ordineId.ordineId
            Ordine.objects.filter(ordineId=id).update(flagStatoOrdine=True)
            return Response({"Avviso":"Ordine completato"},status=status.HTTP_200_OK)
            
    
    return Response(status=status.HTTP_200_OK)
  





