from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class Cliente(AbstractUser):
    clienteId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    ragioneSociale = models.CharField(max_length=200)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Ordine(models.Model):
    ordineId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clienteId = models.ForeignKey(Cliente,on_delete=models.CASCADE)
    dataOrdine = models.DateTimeField(blank=True)
    flagStatoOrdine = models.BooleanField(null=False, default=False)
    indirizzoSpedizione = models.CharField(max_length=200)
    descrizione=models.TextField(blank=True)
    ordinePadre=models.CharField(max_length=30,blank=True)


class StateChoises(models.IntegerChoices):
    INSERITO= 1,'Inserito'
    IN_PRODUZIONE = 2,'In Produzione'
    LOGISTICA_SPEDIZIONE= 3,'Logistica e Spedizione'
    SPEDITO= 4,'Spedito'
class Prodotto(models.Model):

    prodottoId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ordineId = models.ForeignKey(Ordine,on_delete=models.CASCADE,blank=True)
    quantita = models.FloatField(blank=True)
    stato = models.IntegerField(default=StateChoises.INSERITO, choices=StateChoises.choices)
    descrizioneProdotto = models.CharField(max_length=200,blank=True)
    miniatura = models.ImageField(max_length=100,upload_to=None,blank=True) #inserire in upload_to il path dove carichi l'immagine