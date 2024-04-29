from django.db import models
import datetime
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)



class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
    

class Datore(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=30)
    cognome = models.CharField(max_length=30)
    tel = models.IntegerField()
    azienda = models.CharField(max_length=30)

class Offerta(models.Model):
    id = models.AutoField(primary_key=True)
    id_datore = models.ForeignKey(Datore, on_delete=models.CASCADE)
    descrizione = models.CharField(max_length=150)
    data = models.DateTimeField()
    requisiti = models.CharField(max_length=150)

class Candidato (models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=30)
    cognome = models.CharField(max_length=30)
    tel = models.IntegerField()
    residenza = models.CharField(max_length=30)
    competenze = models.CharField(max_length=30)

class Messaggio(models.Model):
    id_datore = models.ForeignKey(Datore, on_delete=models.CASCADE)
    id_candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    id_mittente = models.IntegerField()
    contenuto = models.CharField(max_length=50) 

class Candidatura(models.Model):
    id_candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    id_offerta = models.ForeignKey(Offerta, on_delete=models.CASCADE)
    stato = models.CharField(default="in sospeso", max_length=30)
