from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from aggiornaStato.models import Prodotto, Ordine, Cliente
from aggiornaStato.serializer import OrdineSerializer,ProdottoSerializer,ClienteSerializer
from django.db.models import Q
from itertools import chain 
from django.db import connection
from django.http import JsonResponse

@api_view(['POST'])
def addUtente(request):
    serializer=ClienteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def addOrdine(request):
    serializer=OrdineSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def addProdotto(request):
    serializer=ProdottoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
def getOrdini(request):
    #print(request.headers["ordineId"])
    if request.headers["ordineId"]!="":
        ordine= Ordine.objects.get(ordineId=request.headers["ordineId"])
        cliente= Cliente.objects.get(clienteId=ordine.clienteId.clienteId)
        serializerCliente=ClienteSerializer(cliente).data
        risposta=[{"Ordine":OrdineSerializer(ordine).data,"Cliente":{"ragioneSociale":serializerCliente["ragioneSociale"]}}]
        return Response(risposta)
    
    
    clienti=Cliente.objects.filter(ragioneSociale__icontains=request.headers["ragioneSociale"])
    ordini_date= Ordine.objects.filter(dataOrdine__range=[request.headers["dataFrom"],request.headers["dataTo"]])
    risposta=[]
    for cliente in clienti:
        momentaneo={cliente.ragioneSociale:[]}
        for ordine in ordini_date:
            if ordine.clienteId.clienteId == cliente.clienteId:
                momentaneo[cliente.ragioneSociale].append(OrdineSerializer(ordine).data)
        risposta.append(momentaneo)

    
    return Response(risposta)
    
