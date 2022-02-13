from django.db import models
class SparkPredict(models.Model):

    text = models.CharField(max_length=5000, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)  
    date = models.CharField(max_length=50, null=True, blank=True)
    time =  models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=70, null=True, blank=True)
    prediction = models.IntegerField(default=0)
    class Meta:
        db_table = 'spark_twitter'

class Twitter(models.Model):

    text = models.CharField(max_length=5000)
    name = models.CharField(max_length=50)  
    date = models.CharField(max_length=50)
    time =  models.CharField(max_length=50)
    location = models.CharField(max_length=70)
    class Meta:
        db_table = 'twitter'


