from django import forms
from .models import Uzytkownik

class StworzUzytkownika(forms.ModelForm):
    class Meta:
        model=Uzytkownik

        fields=[
        'email',
        'username',
        'password',
        'first_name',
        'last_name',
        'data_urodzenia'
        ]
