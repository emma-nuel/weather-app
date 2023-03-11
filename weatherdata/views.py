from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import WeatherData
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import WeatherDataSerializer, UserSerializer
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

# Create your views here.

# Homepage 
def homepage(request):
    dataQuerySet = WeatherData.objects.all().last()
    data = {
        "temperature_in_celsius" : dataQuerySet.temperature_in_celsius,
        "temperature_in_farenheit" : dataQuerySet.temperature_in_farenheit,
        "humidity" : dataQuerySet.humidity,
        "heatindex" : dataQuerySet.heatindex,
    }
    return render(request, "homepage.html", context=data)

def update_homepage(request):
    dataQuerySet = WeatherData.objects.all().last()
    data = {
        "temperature_in_celsius" : dataQuerySet.temperature_in_celsius,
        "temperature_in_farenheit" : dataQuerySet.temperature_in_farenheit,
        "humidity" : dataQuerySet.humidity,
        "heatindex" : dataQuerySet.heatindex,
    }
    return render(request, "update_homepage.html", context=data)


#The API View allows only GET and POST
class weatherdataview(APIView):
    
    def get(self, request):
        data =  WeatherData.objects.all()
        serializer = WeatherDataSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WeatherDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class specificuserdataview(APIView):
    
    def get(self, request, username, password):
        data = get_object_or_404(User, username=username)
        # data =  User.objects.all(pk=id)
        print('data:', data.password)
        # print('user   name:', username)
        serializer = UserSerializer(data)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class userdataview(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        data =  User.objects.all()
        print('data:', data)
        serializer = UserSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


