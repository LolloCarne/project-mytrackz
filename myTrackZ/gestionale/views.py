from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from aggiornaStato.models import Prodotto, Ordine, Cliente
from aggiornaStato.serializer import OrdineSerializer,ProdottoSerializer,ClienteSerializer
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


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



def contaProdotti(idOrdine):
    return Prodotto.objects.filter(ordineId=idOrdine).count()


@api_view(['GET'])
def getOrdini(request):
    if request.headers["ordineId"]!="":
        ordine= Ordine.objects.get(ordineId=request.headers["ordineId"])
        cliente= Cliente.objects.get(clienteId=ordine.clienteId.clienteId)
        serializerCliente=ClienteSerializer(cliente).data
        risposta=[{serializerCliente["ragioneSociale"]:[{"ordineId":OrdineSerializer(ordine).data["ordineId"],"dataOrdine":OrdineSerializer(ordine).data["dataOrdine"],"flagStatoOrdine":OrdineSerializer(ordine).data["flagStatoOrdine"],"numeroProdotti":contaProdotti(request.headers["ordineId"]),"ordinePadre":""}]}]
        return Response(risposta)
    
    
    clienti=Cliente.objects.filter(ragioneSociale__icontains=request.headers["ragioneSociale"])
    ordini_date= Ordine.objects.filter(dataOrdine__range=[request.headers["dataFrom"],request.headers["dataTo"]])
    risposta=[]
    for cliente in clienti:
        momentaneo={cliente.ragioneSociale:[]}
        for ordine in ordini_date:
            if ordine.clienteId.clienteId == cliente.clienteId:
                datiOrdine={"ordineId":OrdineSerializer(ordine).data["ordineId"],"dataOrdine":OrdineSerializer(ordine).data["dataOrdine"],"flagStatoOrdine":OrdineSerializer(ordine).data["flagStatoOrdine"],"numeroProdotti":contaProdotti(OrdineSerializer(ordine).data["ordineId"]),"ordinePadre":""}
                momentaneo[cliente.ragioneSociale].append(datiOrdine)
        risposta.append(momentaneo)

    
    return Response(risposta)

@api_view(['GET'])
def getProdotti(request):
    prodotti=Prodotto.objects.filter(ordineId=request.headers["ordineId"])
    risposta=ProdottoSerializer(prodotti,many=True)
    return Response(risposta.data)

@api_view(['GET'])
def getClienti(request):
    utenti= Cliente.objects.filter(ragioneSociale__icontains=request.headers["ragioneSociale"],email__icontains=request.headers["email"])
    risposta=ClienteSerializer(utenti,many=True)
    return Response(risposta.data)

@api_view(['POST'])
def signup(request):
    serializer=ClienteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user=Cliente.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token":token.key,"user":serializer.data})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    user = get_object_or_404(Cliente, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response({"detail":"Not found"},status=status.HTTP_404_NOT_FOUND)
    token, created= Token.objects.get_or_create(user=user)
    serializer=ClienteSerializer(instance=user)

    return Response({"token":token.key,"user":serializer.data})


@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response({})