from django import template
from Witryna.models import Zamowienie

register =template.Library()


@register.filter
def koszyk_zlicz_przedmioty(uzytkownik):
    if uzytkownik.is_authenticated:
        zbior= Zamowienie.objects.filter(uzytkownik=uzytkownik,
                                                 zamowiono=False)
        if zbior.exists():
            return zbior[0].przedmioty.count()
    return 0