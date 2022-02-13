from django.shortcuts import render
from twetter_settings.settings import BASE_DIR
import tweepy
import json
import re
import csv
import time
from kafka import KafkaProducer
import unicodedata
from .models import SparkPredict
from geopy.geocoders import Nominatim

def index(request):
    number_prediction = SparkPredict.objects.filter(prediction=1).count
    total_twitter = SparkPredict.objects.all().count
    twitter_prediction = SparkPredict.objects.filter(prediction=1)
    geolocator = Nominatim(user_agent="app_twetter")
    location = geolocator.geocode("175 5th Avenue NYC")
    teste = {
        "Cota NCH Maracanã FIA": "225,15",
        "PL Junho 2021": "R$ 114,55 MI",
        "Rentabilidade Mês": "-4,56%",
        "Rentabilidade Ano": "15,27%",
        "Rentabilidade ITD": "139,67%",
     }
    context = {'teste': teste}
    return render(request, 'index2.html', context)

def json_serializer(data):
    return json.dumps(data).encode("utf-8")


def clean_tweet(tweet):
    tweet2 = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", str(tweet)).split())
    tweet3 = re.sub(r'^RT[\s]+', '', tweet2)
    return tweet3

def send_to_producer(request):
    auth = tweepy.auth.OAuthHandler('YCRvBi8r0LNZdb4WuYL4bNIEJ', 'VzdKny2yud9vahUfBdnYcJZmwAzFu4NC2KJmqTZEM5CBjSHbPZ')
    auth.set_access_token('1401678034625761280-oCm6rlANlvljtBU5Eso8rQeTGYY5Ae', 'wdkiNklaqpCn4gKTzNd7x1WqZfWb5DOrY2n1LpUVSVz3W')

    api = tweepy.API(auth)

    # Open/create a file to append data to
    # csvFile = open('resultadoFinal.csv', 'a')

    #Use csv writer
    # csvWriter = csv.writer(csvFile)

    producer = KafkaProducer(bootstrap_servers=['kafka:9092'], value_serializer=json_serializer)

    search_words = ["i want to die","i dont want to live anymore","i will kill myself","live","fucking","anyone","bad","shit","tried","suicidal","pain","wish","enough","wanted","die","death","fuck","i dont care","i want to die"]
    #search_words = ["eu quero morrer", "quero me matar","nao quero viver mais", "vou me matar", "viver", "porra", "qualquer um", "mau", "merda", "tentei", "suicida", "dor", "desejo", "suficiente", "queria", "morrer", "morte", "foda-se", "não me importo", "quero morrer"]

    for x in search_words:
        print(x)
        for tweet in tweepy.Cursor(api.search,
                                q =  x,
                                geocode="-22.9110137,-43.2093727,300km",

                                # since = "2021-12-05",
                                #until = "2014-02-15",
                                lang = "en").items(400):

            time.sleep(1)
            twitter_limpo = clean_tweet(tweet.text)
            # Write a row to the CSV file. I use encode UTF-8
            # csvWriter.writerow([tweet.user.screen_name,tweet.created_at, twitter_limpo])

            tweet.user.location = unicodedata.normalize("NFD", tweet.user.location)
            #Essa parte trata a acentuacao das cidades para não quebrar o código
            # print(tweet.user.location) # É o 5º e último. Estava 30°C
            tweet.user.location = tweet.user.location.encode("ascii", "ignore")
            # print(tweet.user.location) # b'E o 5 e ultimo. Estava 30C'
            tweet.user.location = tweet.user.location.decode("utf-8")
            # print(tweet.user.location) # E o 5 e ultimo. Estava 30C

            data = { 'text' : twitter_limpo,
                 'location' : tweet.user.location,
                 'name' : tweet.user.screen_name,
                 'date' : tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }

            # print(data)
            producer.send("Analise-de-Twitter", data)
