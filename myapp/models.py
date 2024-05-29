from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Utente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    azienda = models.CharField(max_length=30 , null=True)
    residenza = models.CharField(max_length=30 , null=True)
    competenze = models.CharField(max_length=30 , null=True)
    tipo = models.CharField(max_length=30 , null=True)

class Offerta(models.Model):
    id = models.AutoField(primary_key=True)
    id_datore = models.ForeignKey(Utente, on_delete=models.CASCADE , related_name='datore_offerta', null=True)
    impiego = models.CharField(max_length=40 , null=True)
    stipendio = models.CharField(max_length=40 , null=True)
    descrizione = models.CharField(max_length=150 , null=True)
    data = models.DateTimeField(null=True)
    requisiti = models.CharField(max_length=150 , null=True)
    luogo = models.CharField(max_length=150 , null=True)

class Messaggio(models.Model):
    id = models.AutoField(primary_key=True)
    id_datore = models.ForeignKey(Utente, on_delete=models.CASCADE , related_name='datore_messaggio', null=False)
    id_candidato = models.ForeignKey(Utente, on_delete=models.CASCADE , related_name='candidato_messaggio',  null=False)
    id_mittente = models.IntegerField(null=True)
    contenuto = models.CharField(max_length=50 , null=True) 

class Candidatura(models.Model):
    id = models.AutoField(primary_key=True)
    id_candidato = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name='candidato_candidatura', null=True)
    id_offerta = models.ForeignKey(Offerta, on_delete=models.CASCADE, null=True, related_name='offerta_candidatura')
    stato = models.CharField(default="in sospeso", max_length=30 , null=True)

class Preferiti(models.Model):
    id = models.AutoField(primary_key=True)
    id_candidato = models.ForeignKey(Utente, on_delete=models.CASCADE, related_name='candidato_preferiti', null=True)
    id_offerta = models.ForeignKey(Offerta, on_delete=models.CASCADE, null=True, related_name='offerta_preferiti')