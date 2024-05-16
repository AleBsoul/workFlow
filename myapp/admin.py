from django.contrib import admin

from .models import  Utente, Candidatura, Messaggio, Offerta

admin.site.register(Utente)
admin.site.register(Candidatura)
admin.site.register(Messaggio)
admin.site.register(Offerta)