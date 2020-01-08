from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.shortcuts import reverse

from string import __all__
# Create your models here.


Kategorie = (
    ('S','Shirt'),
    ('SW', 'Sport-Wear'),
    ('OW', 'Out-Wear')


)
Etykiety = (
    ('P','primary'),
    ('S', 'secondary'),
    ('D', 'danger')

)
class Produkt(models.Model):
    nazwa = models.CharField(max_length=100)
    id    = models.CharField(max_length=10,primary_key=True,)
    opis = models.CharField(max_length=1000,blank=True)
    spefycfikacja = models.CharField(max_length=1000, blank=True)
    zdjecie = models.ImageField(blank=True)
    ilosc = models.IntegerField()
    cena =models.DecimalField(max_digits=10,decimal_places=3)
    promocyjnacena = models.DecimalField(max_digits=10, decimal_places=3,blank=True,null=True)
    kategorie= models.CharField(choices=Kategorie,max_length=2)
    etykieta= models.CharField(choices=Etykiety,max_length=2)

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

class ZamowionyPrzedmiot(models.Model):
    uzytkownik=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    przedmiot=models.ForeignKey(Produkt,on_delete=models.CASCADE)
    ilosc=models.IntegerField(default=1)
    zamowiono=models.BooleanField(default=False)

    def __str__(self):
        return (self.ilosc.__str__()+" of "+self.przedmiot.nazwa)



class Zamowienie(models.Model):
    uzytkownik = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    przedmioty = models.ManyToManyField(ZamowionyPrzedmiot)
    data_zamowienia=models.DateTimeField()
    zamowiono = models.BooleanField(default=False)

