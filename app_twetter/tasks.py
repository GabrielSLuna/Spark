from __future__ import absolute_import, unicode_literals
from twetter_settings.celery import *


def insert_sigla():
    from .models import Locale
    from .views import get_key

    locale = Locale.objects.all()

    for t in locale:
        # print ('------------------', get_key(t.state))
        t.sigla = get_key(t.state)
        t.save()

@app.task()
def task_create_locale():
    from .models import SparkPredict, Locale
    from geopy.geocoders import Nominatim

    twitter = SparkPredict.objects.filter(prediction=1)

    for t in twitter:
        if not Locale.objects.filter(spark_id=t).exists():
            loc = Locale()
            geolocator = Nominatim(user_agent="app_twetter")
            location = geolocator.geocode(t.location, addressdetails=True)

            # lat = adress['lat']
            # lon = adress['lon']
            # display_name = adress['display_name'].split(',')
            try:
                adress = location.raw['address']
            except:
                adress = False
            if adress:
                loc.place_id = location.raw['place_id']
                # loc.lat = lat
                # loc.lon = lon
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
