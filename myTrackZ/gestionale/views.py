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

def contaOrdini(idCliente):
    return Ordine.objects.filter(clienteId=idCliente).count()

@api_view(['GET'])
def getOrdini(request):
    if request.headers["ragioneSociale"] != '':
        clienti=Cliente.objects.filter(ragioneSociale__icontains=request.headers["ragioneSociale"])
        ordini_date= Ordine.objects.filter(dataOrdine__range=[request.headers["dataFrom"],request.headers["dataTo"]],descrizione__icontains=request.headers["descrizione"])
        risposta=[]
        for cliente in clienti:
            momentaneo={cliente.ragioneSociale:[]}
            for ordine in ordini_date:
                if ordine.clienteId.clienteId == cliente.clienteId:
                    datiOrdine={"ordineId":OrdineSerializer(ordine).data["ordineId"],"dataOrdine":OrdineSerializer(ordine).data["dataOrdine"],"flagStatoOrdine":OrdineSerializer(ordine).data["flagStatoOrdine"],"numeroProdotti":contaProdotti(OrdineSerializer(ordine).data["ordineId"]),"descrizione":OrdineSerializer(ordine).data["descrizione"]}
                    momentaneo[cliente.ragioneSociale].append(datiOrdine)
            risposta.append(momentaneo)
    else:
        ordini_date= Ordine.objects.filter(dataOrdine__range=[request.headers["dataFrom"],request.headers["dataTo"]],descrizione__icontains=request.headers["descrizione"])
        risposta=[]
        for ordine in ordini_date:
            cliente=Cliente.objects.get(clienteId=ordine.clienteId.clienteId)
            for risposte in risposta:
                key_list = list(risposte.keys())
                if cliente.ragioneSociale==key_list[0]:
                    risposte[cliente.ragioneSociale].append({cliente.ragioneSociale:[{"ordineId":OrdineSerializer(ordine).data["ordineId"],"dataOrdine":OrdineSerializer(ordine).data["dataOrdine"],"flagStatoOrdine":OrdineSerializer(ordine).data["flagStatoOrdine"],"numeroProdotti":contaProdotti(OrdineSerializer(ordine).data["ordineId"]),"descrizione":OrdineSerializer(ordine).data["descrizione"]}]})
            #datiOrdine={"ordineId":OrdineSerializer(ordine).data["ordineId"],"dataOrdine":OrdineSerializer(ordine).data["dataOrdine"],"flagStatoOrdine":OrdineSerializer(ordine).data["flagStatoOrdine"],"numeroProdotti":contaProdotti(OrdineSerializer(ordine).data["ordineId"]),"ordinePadre":OrdineSerializer(ordine).data["ordinePadre"]}
            risposta.append({cliente.ragioneSociale:[{"ordineId":OrdineSerializer(ordine).data["ordineId"],"dataOrdine":OrdineSerializer(ordine).data["dataOrdine"],"flagStatoOrdine":OrdineSerializer(ordine).data["flagStatoOrdine"],"numeroProdotti":contaProdotti(OrdineSerializer(ordine).data["ordineId"]),"descrizione":OrdineSerializer(ordine).data["descrizione"]}]})
 
    return Response(risposta)

@api_view(['GET'])
def getProdotti(request):
    prodotti=Prodotto.objects.filter(ordineId=request.headers["ordineId"])
    ordine=Ordine.objects.get(ordineId=request.headers["ordineId"])
    ordine_invio={"ordineId":OrdineSerializer(ordine).data["ordineId"],"dataOrdine":OrdineSerializer(ordine).data["dataOrdine"],"flagStatoOrdine":OrdineSerializer(ordine).data["flagStatoOrdine"],"numeroProdotti":contaProdotti(OrdineSerializer(ordine).data["ordineId"]),"descrizione":OrdineSerializer(ordine).data["descrizione"]}
    risposta=[]
    risposta.append(ordine_invio)
    for prodotto in prodotti:
        risposta.append(ProdottoSerializer(prodotto).data)
    
    return Response(risposta)

@api_view(['GET'])
def getClienti(request):
    utenti= Cliente.objects.filter(ragioneSociale__icontains=request.headers["ragioneSociale"],email__icontains=request.headers["email"])
    #clienti=ClienteSerializer(utenti,many=True)
    risposta=[]
    for cliente in utenti:
        oggetto={"ragioneSociale":ClienteSerializer(cliente).data["ragioneSociale"],"email":ClienteSerializer(cliente).data["email"],"clienteId":ClienteSerializer(cliente).data["clienteId"],"numeroOrdini":contaOrdini(ClienteSerializer(cliente).data["clienteId"])}
        risposta.append(oggetto)
        
    return Response(risposta)

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