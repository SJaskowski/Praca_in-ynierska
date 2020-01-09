from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from .views import OknoGlowne,DetaleProduktu,dodaj_do_koszyka,usun_z_koszyka,PodsumowanieZamowienia,DokonaniePlatnosci,usun_pojedynczy_przedmiot_z_koszyka
app_name = "Witryna"
urlpatterns = [
    path('',OknoGlowne.as_view()),
    path('produkt/<pk>',DetaleProduktu.as_view(),name='produkt'),
    path('dodaj_do_koszyka/<pk>',dodaj_do_koszyka,name='dodaj_do_koszyka'),
    path('usun_z_koszyka/<pk>',usun_z_koszyka,name='usun_z_koszyka'),
    path('podsumowanie/',PodsumowanieZamowienia.as_view(),name='podsumowanie_zamowienia'),
    path('dokonaj_platnosci/',DokonaniePlatnosci.as_view(),name='dokonaj_platnosci'),
    path('usun_pojedynczy_przedmiot_z_koszyka/<pk>', usun_pojedynczy_przedmiot_z_koszyka, name='usun_pojedynczy_przedmiot_z_koszyka'),




]