from rest_framework import serializers
from .models import WeatherData
from django.contrib.auth.models import User


class WeatherDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WeatherData
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', "date_joined"]