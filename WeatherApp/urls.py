"""WeatherApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.urls import path
from weatherdata.views import *
from rest_framework.schemas import get_schema_view


urlpatterns = [
    path('', homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('draw-celsius-chart/', draw_celsius_chart, name='draw_celsius_chart'),
    path('draw-farenheit-chart/', draw_farenheit_chart, name='draw_farenheit_chart'),
    path('draw-humidity-chart/', draw_humidity_chart, name='draw_humidity_chart'),
    path('draw-heatindex-chart/', draw_heatindex_chart, name='draw_heatindex_chart'),
    path('line/', line_chart, name="linechart"),
]

# htmx_urlpatterns = [
#     path('update-homepage/', update_homepage, name='update-homepage'),
# ]

restapi_urlpatterns = [
    path(r'logs/', weatherdataview.as_view(), name='logs'),
    path(r'users/<str:username>/', specificuserdataview.as_view(), name='specific_user'),
    path(r'users/', userdataview.as_view(), name='users'),
]

openapi_schema_urlpatterns = [
    path('docs/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
        ), name='swagger-ui'),
    path(r'openapi-schema', get_schema_view(
        title="Weather App",  # Title of your app
        description="Weather Data API",  # Description of your app
        version="1.0.0",
        public=True,
    ), name='openapi-schema')
]

urlpatterns += htmx_urlpatterns
urlpatterns += restapi_urlpatterns
urlpatterns += openapi_schema_urlpatterns