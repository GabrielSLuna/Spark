from django.db import models

class Funds(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=50)  
    country = models.CharField(max_length=50)
    isin =  models.CharField(max_length=50, primary_key=True)
    issuer = models.CharField(max_length=70)

class HistoricalData(models.Model):
    funds_id = models.ForeignKey(Funds, on_delete=models.CASCADE, db_column='funds_id', related_name='funds_id')
    date = models.DateField()
    close = models.FloatField()

