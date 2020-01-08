from django.contrib import admin
from .models import Produkt,Uzytkownik,Zamowienie,ZamowionyPrzedmiot

# Register your models here.

admin.site.register(Produkt)
admin.site.register(Uzytkownik)
admin.site.register(Zamowienie)
admin.site.register(ZamowionyPrzedmiot)