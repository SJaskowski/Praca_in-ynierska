from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from .views import OknoGlowne,DetaleProduktu,dodaj_do_koszyka,\
    usun_z_koszyka,PodsumowanieZamowienia,SzczegolyDostawy,\
    usun_pojedynczy_przedmiot_z_koszyka,DokojnajPlatnosci,paypall_sukces,paypall_powrot,\
    oproznij_koszyk,zmien_kategorie

app_name = "Witryna"
urlpatterns = [
    path('',OknoGlowne.as_view(),name="Main"),
    path('produkt/<pk>',DetaleProduktu.as_view(),name='produkt'),
    path('dodaj_do_koszyka/<pk>',dodaj_do_koszyka,name='dodaj_do_koszyka'),
    path('usun_z_koszyka/<pk>',usun_z_koszyka,name='usun_z_koszyka'),
    path('podsumowanie/',PodsumowanieZamowienia.as_view(),name='podsumowanie_zamowienia'),
    path('szczegoly_dostawy/', SzczegolyDostawy.as_view(), name='szczegoly_dostawy'),
    path('usun_pojedynczy_przedmiot_z_koszyka/<pk>', usun_pojedynczy_przedmiot_z_koszyka, name='usun_pojedynczy_przedmiot_z_koszyka'),
    path('zaplac/', DokojnajPlatnosci, name='dokonaj_platnosci'),
    path('oproznij_koszyk/', oproznij_koszyk, name='oproznij_koszyk'),
    path('zaplac/paypal/powrot', paypall_powrot, name='paypall_powrot'),
    path('zaplac/paypal/sukces', paypall_sukces, name='paypall_sukces'),
    path('zmien_kategorie/<str:kategoria>', zmien_kategorie, name='zmien_kategorie'),






]