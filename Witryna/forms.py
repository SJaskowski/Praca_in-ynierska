from django import forms
from .models import Uzytkownik
from django_countries.fields import CountryField

Wybor_Platonosci=(
    ('P','Przelew'),
    ('PP','Paypal'),
    ('OD','Płatność przy odbiorze')

)

class FormularzDanychAdresowych(forms.Form):
    nazwa_ulicy = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Nazwa Ulicy"}),required=False)
    imie = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder':"Imie"}),required=False)
    nazwisko = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder':"Nazwisko"}),required=False)
    nr_domu =forms.CharField(widget=forms.TextInput(attrs={'placeholder':"NrDomu/NrMieszkania"}),required=False)
    kraj = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Kraj"}),required=False)
    kod_pocztowy = forms.CharField(max_length=6,widget=forms.TextInput(attrs={'placeholder': "XX-XXX"}),required=False)
    miasto = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Miasto"}),required=False)
    zapamietaj_adres = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
    rodzaj_platnosci=forms.ChoiceField(choices=Wybor_Platonosci,widget=forms.RadioSelect)
    uzyj_zapamietanego = forms.BooleanField(widget=forms.CheckboxInput(),required=False)

class FormularzFiltraPrzedmiotów(forms.Form):
    szukany_przedmiot = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Szukaj"}))

