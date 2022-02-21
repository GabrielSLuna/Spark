from __future__ import annotations
from ast import Delete
from django.db import models
class SparkPredict(models.Model):
    tweet = models.CharField(max_length=5000, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)  
    date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=70, null=True, blank=True)
    prediction = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'spark_twitter'
        ordering = ['date']
    
class Locale(models.Model):
    country = models.CharField(max_length=70, blank=True, null=True)  
    state = models.CharField(max_length=70, blank=True, null=True)
    city = models.CharField(max_length=70, blank=True, null=True)
    place_id = models.IntegerField(blank=True, null=True)
    sigla = models.CharField(max_length=10, blank=True, null=True)
    spark_id = models.ForeignKey(SparkPredict, on_delete=models.CASCADE)
    class Meta:
        db_table = 'twitter_location'




