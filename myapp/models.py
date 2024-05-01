from django.db import models
from django.utils import timezone


class Datore(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=20 , null=True)
    cognome = models.CharField(max_length=20 , null=True)
    email = models.CharField(max_length=60 , null=True)
    username =  models.CharField(max_length=20 , null=True)
    password = models.CharField(max_length=20 , null=True)
    azienda = models.CharField(max_length=30 , null=True)

class Offerta(models.Model):
    id = models.AutoField(primary_key=True)
    id_datore = models.ForeignKey(Datore, on_delete=models.CASCADE , null=True)
    descrizione = models.CharField(max_length=150 , null=True)
    data = models.DateTimeField(null=True)
    requisiti = models.CharField(max_length=150 , null=True)

class Candidato (models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=30 , null=True)
    cognome = models.CharField(max_length=30 , null=True)
    email = models.CharField(max_length=60 , null=True)
    username =  models.CharField(max_length=20 , null=True)
    password = models.CharField(max_length=20 , null=True)
    residenza = models.CharField(max_length=30 , null=True)
    competenze = models.CharField(max_length=30 , null=True)

class Messaggio(models.Model):
    id_datore = models.ForeignKey(Datore, on_delete=models.CASCADE , null=True)
    id_candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE , null=True)
    id_mittente = models.IntegerField(null=True)
    contenuto = models.CharField(max_length=50 , null=True) 

class Candidatura(models.Model):
    id_candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    id_offerta = models.ForeignKey(Offerta, on_delete=models.CASCADE , null=True)
    stato = models.CharField(default="in sospeso", max_length=30 , null=True)