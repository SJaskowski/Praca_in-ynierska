from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Produkt,ZamowionyPrzedmiot,Zamowienie,Adres
from django.views.generic import ListView,DetailView,View
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .forms import FormularzDanychAdresowych
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings



class OknoGlowne(ListView):
    model = Produkt
    paginate_by = 5
    template_name = "Strona_glowna.html"

class DetaleProduktu(DetailView):
        model = Produkt
        template_name = "Produkt_detale.html"
@login_required()
def dodaj_do_koszyka(request, pk):
    produkt = get_object_or_404(Produkt,id=pk)
    if produkt.ilosc>0:
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
                    produkt.ilosc -= 1
                    produkt.save()
                    return redirect("Witryna:podsumowanie_zamowienia")
                else:
                    zamowienia.przedmioty.add(zamowiony_przedmiot)
                    messages.info(request, "dodano przedmiot do koszyka")
                    produkt.ilosc -= 1
                    produkt.save()
                    return redirect("Witryna:produkt", pk)
        else:
            data_zamowienia = timezone.now()
            zamowienia = Zamowienie.objects.create(uzytkownik=request.user,data_zamowienia=data_zamowienia)
            zamowienia.przedmioty.add(zamowiony_przedmiot)
            messages.info(request, "dodano przedmiot do koszyka")
            produkt.ilosc -= 1
            produkt.save()
            return redirect("Witryna:produkt", pk)
    else:
        messages.error(request, "Produkt niedostepny")
        return redirect("Witryna:produkt", pk)


@login_required()
def usun_z_koszyka(request,pk):
    produkt = get_object_or_404(Produkt, id=pk)
    zamowienie_zbior = Zamowienie.objects.filter(uzytkownik=request.user,
                                                 zamowiono=False)
    if zamowienie_zbior.exists():
        zamowienia = zamowienie_zbior[0]
        if zamowienia.przedmioty.filter(przedmiot__id=produkt.id).exists():
            zamowiony_przedmiot=ZamowionyPrzedmiot.objects.filter(przedmiot=produkt,
                                                            uzytkownik=request.user,
                                                            zamowiono=False)[0]

            produkt.ilosc =produkt.ilosc + zamowiony_przedmiot.ilosc
            produkt.save()
            zamowiony_przedmiot.ilosc = 1
            zamowiony_przedmiot.save()
            zamowienia.przedmioty.remove(zamowiony_przedmiot)

        else:
            return redirect("Witryna:podsumowanie_zamowienia")

    else:

        return redirect("Witryna:podsumowanie_zamowienia")

    return redirect("Witryna:podsumowanie_zamowienia")


class PodsumowanieZamowienia(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            zamowienia = Zamowienie.objects.get(uzytkownik=self.request.user,
                                                   zamowiono=False)
            contex={
            'object': zamowienia

            }
            return render(self.request, "podsumowanie_zamowienia.html", contex)
        except ObjectDoesNotExist:
            messages.error(self.request,"Koszyk jest pusty")
            return redirect("/")


class SzczegolyDostawy(View):

    def get(self,*args,**kwargs):
        formularz=FormularzDanychAdresowych()
        contex = {
            'formularz': formularz

        }
        return render(self.request, "daneAdresowe.html",contex)

    def post(self,*args,**kwargs):
        formularz = FormularzDanychAdresowych(self.request.POST or None)

        try:
            zamowienia = Zamowienie.objects.get(uzytkownik=self.request.user,
                                                  zamowiono=False)

            if formularz.is_valid():
                nazwa_ulicy = formularz.cleaned_data.get('nazwa_ulicy')
                nr_domu = formularz.cleaned_data.get('nr_domu')
                kraj = formularz.cleaned_data.get('kraj')
                kod_pocztowy = formularz.cleaned_data.get('kod_pocztowy')
                miasto = formularz.cleaned_data.get('miasto')
                zapamietaj_adres=formularz.cleaned_data.get('zapamietaj_adres')
                rodzaj_platnosci=formularz.cleaned_data.get('rodzaj_platnosci')
                adres = Adres(
                    uzytkownik=self.request.user,
                    nazwa_ulicy=nazwa_ulicy,
                    nr_domu=nr_domu,
                    kraj=kraj,
                    kod_pocztowy=kod_pocztowy,
                    miasto=miasto,
                    zapamietano=zapamietaj_adres
                )
                adres.save()
                return redirect('Witryna:dokonaj_platnosci')
            messages.warning(self.request, "Nie poprawnie uzupełniony formluarz")
            return redirect('Witryna:dokonaj_platnosci')
        except ObjectDoesNotExist:
            messages.error(self.request,"Nie posiadasz Zamowienia")
            return redirect ("Witryna:podsumowanie_zamowienia")

@login_required()
def usun_pojedynczy_przedmiot_z_koszyka(request, pk):
    produkt = get_object_or_404(Produkt, id=pk)
    zamowienie_zbior = Zamowienie.objects.filter(uzytkownik=request.user,
                                                 zamowiono=False)
    if zamowienie_zbior.exists():
        zamowienia = zamowienie_zbior[0]
        if zamowienia.przedmioty.filter(przedmiot__id=produkt.id).exists() :
            zamowiony_przedmiot=ZamowionyPrzedmiot.objects.filter(przedmiot=produkt,
                                                    uzytkownik=request.user,
                                                    zamowiono=False)[0]
            if zamowiony_przedmiot.ilosc>1:
                zamowiony_przedmiot.ilosc -= 1
                produkt.ilosc += 1
                produkt.save()
                zamowiony_przedmiot.save()

        else:
            return redirect("Witryna:podsumowanie_zamowienia")

    else:

        return redirect("Witryna:podsumowanie_zamowienia")

    return redirect("Witryna:podsumowanie_zamowienia")

def DokojnajPlatnosci(request):
        try:
            zamowienia = Zamowienie.objects.get(uzytkownik=request.user,
                                                   zamowiono=False)
            id_zamowienia=zamowienia.get_id()
            paypal_dict = {
                "business": settings.PAYPAL_RECEIVER_EMAIL,
                "amount": zamowienia.cena_koncowa_zamowienia,
                "item_name": "Zamówienie nr",
                "invoice": id_zamowienia,
                "currency_code":"PLN",
                "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                "return": request.build_absolute_uri(reverse('Witryna:paypall_sukces')),
                "cancel_return": request.build_absolute_uri(reverse('Witryna:paypall_powrot')),

            }
            formularz=PayPalPaymentsForm(initial=paypal_dict)
            return render(request,'zaplata.html',{'zamowienie':zamowienia,'formularz':formularz})
        except ObjectDoesNotExist:
            messages.error(request,"Koszyk jest pusty")
            return redirect("/")


@login_required()
def oproznij_koszyk(request):
        zamowienie_zbior = Zamowienie.objects.filter(uzytkownik=request.user, zamowiono=False).delete()
        zamowiony_przedmiot = ZamowionyPrzedmiot.objects.filter(uzytkownik=request.user, zamowiono=False).delete()
        return redirect("Witryna:podsumowanie_zamowienia")

@csrf_exempt
@login_required()
def paypall_sukces(request):
    aktualizuj_status(request)
    # oproznij_koszyk(request)
    return render(request,"PayPalSukces.html")
@csrf_exempt
@login_required()
def paypall_powrot(request):
    return render(request,"PayPalPowrót.html")

@login_required()
def aktualizuj_status(request):
    zamowienia = Zamowienie.objects.get(uzytkownik=request.user,
                                        zamowiono=False)
    zamowienia.aktualizuj_status_zamowienia()

