from django import forms
from .models import Uzytkownik
from django_countries.fields import CountryField

Wybor_Platonosci=(
    ('P','Przelew'),
    ('PP','Paypal'),
    ('OD','Płatność przy odbiorze')

)

class FormularzDanychAdresowych(forms.Form):
    nazwa_ulicy = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Nazwa Ulicy"}))
    nr_domu =forms.CharField(widget=forms.TextInput(attrs={'placeholder':"NrDomu/NrMieszkania"}))
    kraj = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Kraj"}))
    kod_pocztowy = forms.CharField(max_length=6,widget=forms.TextInput(attrs={'placeholder': "XX-XXX"}))
    miasto = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Miasto"}))
    zapamietaj_adres = forms.BooleanField(widget=forms.CheckboxInput())
    rodzaj_platnosci=forms.ChoiceField(choices=Wybor_Platonosci,widget=forms.RadioSelect)

