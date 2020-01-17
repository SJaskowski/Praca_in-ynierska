from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.shortcuts import reverse
from django import forms

from string import __all__
# Create your models here.



class Kategoria(models.Model):
    nazwa=models.CharField(max_length=100)
    id=models.CharField(max_length=3,primary_key=True)

    def zmien_kategorie_url(self):
            return reverse("Witryna:zmien_kategorie", kwargs={
                'kategoria': self.nazwa
            })
    def podstawowa_kategorie_url(self):
            return reverse("Witryna:podstawowa_kategorie", kwargs={
                'kategoria': 3
            })

class Produkt(models.Model):
    nazwa = models.CharField(max_length=100)
    id    = models.CharField(max_length=10,primary_key=True,)
    opis = models.CharField(max_length=1000,blank=True)
    spefycfikacja = models.CharField(max_length=1000, blank=True)
    zdjecie = models.ImageField(blank=True)
    ilosc = models.IntegerField()
    cena =models.DecimalField(max_digits=10,decimal_places=2)
    promocyjnacena = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    kategoria= models.ForeignKey(Kategoria,on_delete=models.CASCADE)


    def __str__(self):
        return self.nazwa

    def get_absolute_url(self):
        return reverse("Witryna:produkt",kwargs={
            'pk':self.id
        })
    def get_dodaj_do_koszyka_url(self):
            return reverse("Witryna:dodaj_do_koszyka", kwargs={
                'pk': self.id
            })


    def get_usun_z_koszykaa_url(self):
        return reverse("Witryna:usun_z_koszyka", kwargs={
            'pk': self.id
        })


class Uzytkownik(AbstractUser):
  data_urodzenia = models.DateField(null=True, blank=True)

  def __str__(self):
      return self.username


class Adres(models.Model):
    uzytkownik=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    imie=models.CharField(max_length=100)
    nazwisko=models.CharField(max_length=100)
    nazwa_ulicy=models.CharField(max_length=100)
    nr_domu=models.CharField(max_length=100)
    kraj=models.CharField(max_length=100)
    kod_pocztowy=models.CharField(max_length=6)
    miasto=models.CharField(max_length=100)
    zapamietano=models.BooleanField(default=False)



class ZamowionyPrzedmiot(models.Model):
    uzytkownik=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    przedmiot=models.ForeignKey(Produkt,on_delete=models.CASCADE)
    ilosc=models.IntegerField(default=1)
    zamowiono=models.BooleanField(default=False)

    def cena_calkowita_produktow(self):
        if self.przedmiot.promocyjnacena:
         return self.ilosc * self.przedmiot.promocyjnacena
        else:
         return self.ilosc * self.przedmiot.cena
    def __str__(self):
        return (self.ilosc.__str__()+" razy "+self.przedmiot.nazwa)

    def oszczedzonakwota(self):
        if self.przedmiot.promocyjnacena:
            return (self.przedmiot.cena*self.ilosc)-(self.przedmiot.promocyjnacena*self.ilosc)
        else:
            return 0;

    def aktualizuj_status_zamowienia(self):
        self.zamowiono = True
        self.save()


class Zamowienie(models.Model):
    uzytkownik = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_zamowienia = models.DateTimeField()

    przedmioty = models.ManyToManyField(ZamowionyPrzedmiot)

    zamowiono = models.BooleanField(default=False)
    adres=models.ForeignKey('Adres',on_delete=models.SET_NULL,blank=True,null=True)
    id_zamowienia = uzytkownik.__str__() + str(data_zamowienia)
    def cena_koncowa_zamowienia(self):
        suma=0
        for zamowienie in self.przedmioty.all():
            suma +=zamowienie.cena_calkowita_produktow()

        return suma

    def get_id(self):
        return self.id_zamowienia

    def aktualizuj_status_zamowienia(self):
        self.zamowiono=True
        self.save()