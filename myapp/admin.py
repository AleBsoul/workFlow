from django.contrib import admin

from .models import  Utente, Candidatura, Messaggio, Offerta, Preferiti

admin.site.register(Utente)
admin.site.register(Candidatura)
admin.site.register(Messaggio)
admin.site.register(Offerta)
admin.site.register(Preferiti)
