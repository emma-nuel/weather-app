from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class WeatherData(models.Model):
    temperature_in_celsius = models.FloatField()
    temperature_in_farenheit = models.FloatField()
    humidity = models.FloatField()
    heatindex = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
