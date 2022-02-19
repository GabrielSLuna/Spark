from __future__ import absolute_import, unicode_literals
from twetter_settings.celery import *

@app.task()
def task_create_locale():
    from .models import SparkPredict, Locale
    from geopy.geocoders import Nominatim

    twitter = SparkPredict.objects.filter(prediction=1)

    for t in twitter:
        if not Locale.objects.filter(spark_id=t).exists():
            loc = Locale()
            geolocator = Nominatim(user_agent="app_twetter")
            location = geolocator.geocode(t.location)

            lat = location.raw['lat']
            lon = location.raw['lon']
            display_name = location.raw['display_name'].split(',')

            loc.place_id = location.raw['place_id']
            loc.lat = lat
            loc.lon = lon
            loc.country = display_name[-1]
            loc.state = display_name[5]
            loc.city = display_name[0]
            loc.spark_id = t
            loc.save()
