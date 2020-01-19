from django.contrib import admin
from .models import Produkt,Uzytkownik,Zamowienie,ZamowionyPrzedmiot,Kategoria,Adres,KontoBankowe

# Register your models here.

class ZamowienieAdmin(admin.ModelAdmin):
    list_display = ['uzytkownik',
                    'zamowiono',
                    'zaplacono',
                    'id_zamowienia',
                    'data_zamowienia',
                    'adres'

                    ]
    list_display_links = [
        'uzytkownik',
        'adres',


    ]
class AdresAdmin(admin.ModelAdmin):
    list_display = ['uzytkownik',
                    'imie',
                    'nazwisko',
                    'nazwa_ulicy',
                    'nr_domu',
                    'kraj',
                    'kod_pocztowy',
                    'miasto',
                    'zapamietano',


                     ]
class ProduktAdmin(admin.ModelAdmin):

    list_display = [ 'nazwa',
                    'ilosc',
                     'cena',
                     'promocyjnacena',
                     'kategoria'
    ]

admin.site.register(Produkt,ProduktAdmin)
admin.site.register(Uzytkownik)
admin.site.register(Zamowienie,ZamowienieAdmin)
admin.site.register(ZamowionyPrzedmiot)
admin.site.register(KontoBankowe)
admin.site.register(Adres,AdresAdmin)
admin.site.register(Kategoria)