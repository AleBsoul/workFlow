from django.contrib import admin

from .models import  Candidato, Datore, Candidatura, Messaggio, Offerta

admin.site.register(Candidato)
admin.site.register(Datore)
admin.site.register(Candidatura)
admin.site.register(Messaggio)
admin.site.register(Offerta)