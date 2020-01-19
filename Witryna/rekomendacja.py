import redis
from django.conf import settings
from .models import Produkt


polaczenie = redis.StrictRedis(host=settings.REDIS_HOST,
                               port=settings.REDIS_PORT,
                               db=settings.REDIS_DB)

class   Rekomendacja(object):
    def get_klucz_produktu(self, ip):
        return 'Produkt:{}: kupowano z'.format(ip)

    def produkty_zakupione(self,zamowione_przedmioty):
        produkty=zamowione_przedmioty
        id_produktow = [p for p in produkty]
        for id_produktu in id_produktow:
            for with_id in id_produktow:
                if id_produktu != with_id:
                    polaczenie.zincrby(self.get_klucz_produktu(id_produktu),
                                       1,
                                       with_id)

    def sugeruj_produkty(self,produkt,max_wynikow=6):

        # id_produktow= [p.id for p in produkty]
        # id_produktow[0]
        # if len(produkty) == 1:
        rekomendacja = polaczenie.zrange(self.get_klucz_produktu(produkt),0,-1,desc=True)[:max_wynikow]

        # else:
        #     flat_ids = ''.join([str(id) for id in id_produktow])
        #     klucz_tymczasowy = 'tmp_{}'.format(flat_ids)
        #     klucze = [self.get_klucz_produktu(id) for id in id_produktow]
        #     polaczenie.zunionstore(klucz_tymczasowy,klucze)
        #     polaczenie.zrem(klucz_tymczasowy, *id_produktow)
        #     rekomendacja= polaczenie.zrange(klucz_tymczasowy,0,-1,desc=True)[:max_wynikow]
        #     polaczenie.delete(klucz_tymczasowy)
        rekomendowane_id_produktow = [id for id in rekomendacja]
        produkty=  Produkt.objects.all()
        rekomendowane_produkty= []
        for object in rekomendowane_id_produktow:
            tmp=str(object)
            tmp.strip("'")
            print(tmp[2:len(tmp)-1])
            rekomendowane_produkty+=produkty.filter(id=tmp[2:len(tmp)-1])
        return rekomendowane_produkty

    def usun_rekoemndacje(self):
        for id in Produkt.objects.values_list('id',flat=True):
            polaczenie.delete(self.get_klucz_produktu(id))

