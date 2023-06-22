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
    clienteId = models.ForeignKey("Cliente",on_delete=models.CASCADE)
    dataOrdine = models.DateTimeField(blank=True)
    flagStatoOrdine = models.BooleanField(null=False, default=False)
    indirizzoSpedizione = models.CharField(max_length=200)

class Prodotto(models.Model):
    STATE_CHOISES = [
        ('I','Inserito'),
        ('P','In Produzione'),
        ('L','Logistica e Spedizione'),
        ('S','Spedito')
    ]
    prodottoId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ordineId = models.ForeignKey("Ordine",on_delete=models.CASCADE)
    quantita = models.FloatField()
    stato = models.CharField(max_length=1,choices=STATE_CHOISES)
    descrizioneProdotto = models.CharField(max_length=200)
    miniatura = models.ImageField(max_length=100,upload_to=None) #inserire in upload_to il path dove carichi l'immagine