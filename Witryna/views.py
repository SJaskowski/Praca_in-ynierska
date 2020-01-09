from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Produkt,ZamowionyPrzedmiot,Zamowienie
from django.views.generic import ListView,DetailView
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout



class OknoGlowne(ListView):
    model = Produkt
    template_name = "Strona_glowna.html"

class DetaleProduktu(DetailView):
        model = Produkt
        template_name = "Produkt_detale.html"

def dodaj_do_koszyka(request, pk):
    produkt = get_object_or_404(Produkt,id=pk)
    zamowiony_przedmiot, created=ZamowionyPrzedmiot.objects.get_or_create(przedmiot=produkt,
                                                                 uzytkownik=request.user,
                                                                 zamowiono=False)
    zamowienie_zbior = Zamowienie.objects.filter(uzytkownik=request.user,
                                                 zamowiono=False)
    if zamowienie_zbior.exists():
            zamowienia=zamowienie_zbior[0]
            if zamowienia.przedmioty.filter(przedmiot__id=produkt.id).exists():
                zamowiony_przedmiot.ilosc += 1
                zamowiony_przedmiot.save()
                messages.info(request, "dodano przedmiot do koszyka")
                return redirect("Witryna:produkt", pk)
            else:
                zamowienia.przedmioty.add(zamowiony_przedmiot)
                messages.info(request, "dodano przedmiot do koszyka")
                return redirect("Witryna:produkt", pk)
    else:
        data_zamowienia = timezone.now()
        zamowienia = Zamowienie.objects.create(uzytkownik=request.user,data_zamowienia=data_zamowienia)
        zamowienia.przedmioty.add(zamowiony_przedmiot)
        messages.info(request, "dodano przedmiot do koszyka")
        return redirect("Witryna:produkt", pk)



def usun_z_koszyka(request,pk):
    produkt = get_object_or_404(Produkt, id=pk)
    zamowienie_zbior = Zamowienie.objects.filter(uzytkownik=request.user,
                                                 zamowiono=False)
    if zamowienie_zbior.exists():
        zamowienia = zamowienie_zbior[0]
        if zamowienia.przedmioty.filter(przedmiot__id=produkt.id).exists():
            zamowiony_przedmiot=ZamowionyPrzedmiot.filter.get_or_create(przedmiot=produkt,
                                                    uzytkownik=request.user,
                                                    zamowiono=False)[0]
            zamowienia.przedmioty.remove(zamowiony_przedmiot)
        else:
            return redirect("Witryna:produkt", pk)

    else:

        return redirect("Witryna:produkt", pk)

    return redirect("Witryna:produkt", pk)
