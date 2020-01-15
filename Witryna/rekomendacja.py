import redis
from django.conf import settings
from .models import Produkt


polaczenie = redis.StrictRedis(host=settings.REDIS_HOST,
                               post=settings.REDIS_PORT,
                               db=settings.REDIS_DB)

class  Rekomendacja(object):
    def get_klucz_produktu(self,id):
        return 'Produkt:{}: kupowano z'.format(id)

    def produkty_zakupione(self,produkty):
        id_produktow = [p.id for p in produkty]
        for id_produktu in id_produktow:
            for z_id in id_produktow:
                if id_produktu != z_id:
                    polaczenie.zincrby(self.get_klucz_produktu(id_produktu),z_id,ilosc=1)

    def sugeruj_produkty(self,produkty,max_wynikow=6):
        id_produktow= [p.id for p in produkty]
        if len(produkty) == 1:
            rekomendacja = polaczenie.zrange(self.get_klucz_produktu(id_produktow[0]),0,-1,desc=True)[:max_wynikow]

        else:
            flat_ids = ''.join([str(id) for id in id_produktow])
            klucz_tymczasowy = 'tmp_{}'.format(flat_ids)
            klucze = [self.get_klucz_produktu(id) for id in id_produktow]
            polaczenie.zunionstore(klucz_tymczasowy,klucze)
            polaczenie.zrem(klucz_tymczasowy, *id_produktow)
            rekomendacja= polaczenie.zrange(klucz_tymczasowy,0,-1,desc=True)[:max_wynikow]
            polaczenie.delete(klucz_tymczasowy)
        rekomendowane_id_produktow = [int(id) for id in rekomendacja]
        rekomendowane_produkty  =  list(Produkt.objects.filter(id=rekomendowane_id_produktow))
        rekomendowane_produkty.sort(key=lambda x: rekomendowane_id_produktow.index(x.id))
        return rekomendowane_produkty

    def usun_rekoemndacje(self):
        for id in Produkt.objects.values_list('id',flat=True):
            polaczenie.delete(self.get_klucz_produktu(id))

