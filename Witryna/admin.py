from django.contrib import admin
from .models import Produkt,Uzytkownik,Zamowienie,ZamowionyPrzedmiot,Kategoria

# Register your models here.

class ZamowienieAdmin(admin.ModelAdmin):
    list_display = ['uzytkownik','zamowiono']

admin.site.register(Produkt)
admin.site.register(Uzytkownik)
admin.site.register(Zamowienie,ZamowienieAdmin)
admin.site.register(ZamowionyPrzedmiot)
admin.site.register(Kategoria)