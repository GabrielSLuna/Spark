from __future__ import absolute_import, unicode_literals
from twetter_settings.celery import *


def insert_sigla():
    from .models import Locale
    from .views import get_key

    locale = Locale.objects.all()

    for t in locale:
        t.sigla = get_key(t.state)
        t.save()

def do_geocode(address):
    from geopy.exc import GeocoderTimedOut
    from geopy.geocoders import Nominatim

    try:
        geolocator = Nominatim(user_agent="app_twetter")
        adr = address
        adr = adr.replace('amanbai ', '')
        return geolocator.geocode(adr, addressdetails=True, timeout=None)
    except GeocoderTimedOut:
        return ''
        # return do_geocode(address)

@app.task()
def task_create_locale():
    from .models import SparkPredict, Locale

    print('--------Iniciando task_create_locale')

    twitter = SparkPredict.objects.filter(prediction=1)

    for t in twitter:
        if not Locale.objects.filter(spark_id=t).exists():
            loc = Locale()
            if t.location and t.location != "":
                location = do_geocode(t.location)
                if not location:
                    continue
            else:
                continue
            try:
                adress = location.raw['address']
            except:
                adress = False
            if adress:
                loc.place_id = location.raw['place_id']
                try:
                    loc.country = adress['country']
                except:
                    loc.country = ''
                try:
                    loc.state = adress['state']
                except:
                    loc.state = ''
                try:
                    loc.city = adress['city']
                except:
                    loc.city = ''
            
                loc.spark_id = t
                loc.save()

    insert_sigla()
