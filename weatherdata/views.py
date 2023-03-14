from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import WeatherData
from .serializers import WeatherDataSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
import plotly.express as px
import datetime
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import DatetimeTickFormatter, HoverTool, ColumnDataSource
# Create your views here.

# Homepage 
def homepage(request):
    dataQuerySet = WeatherData.objects.all().last()
    chart_queryset = WeatherData.objects.all()    

    temperatures = [item.temperature_in_celsius for item in chart_queryset]
    farenheit_temperatures = [item.temperature_in_farenheit for item in chart_queryset]
    humidities = [item.humidity for item in chart_queryset]
    heatindexes = [item.heatindex for item in chart_queryset]
    dates = [val.timestamp for val in chart_queryset]


    #General Data Source
    chart_data = ColumnDataSource(data = dict(temperature = temperatures, date = dates, farenheit_temperature = farenheit_temperatures, humidity=humidities, heatindex=heatindexes))
    
    fig = figure(width=400, 
                 height=400, 
                 x_axis_type="datetime",
                 )

    fig.line(
        source = chart_data,
        x='date',
        y='temperature',
        line_width = 2,
        
    )

    fig.title.align = 'center'
    fig.title.text_font_size = '1em' 
    fig.toolbar_location="above"
    fig.toolbar.autohide = True
    fig.xaxis.formatter = DatetimeTickFormatter(days="%b %d")


    tooltips = [
        ('Temperature', '@temperature'),
        ('Date', '@date{%F}')
    ]
    fig.add_tools(HoverTool(tooltips=tooltips, formatters={'@date' : 'datetime'}))

    farenheit_fig = figure(width=400, 
                 height=400, 
                 x_axis_type="datetime",
                 )

    farenheit_fig.line(
        source = chart_data,
        x='date',
        y='farenheit_temperature',
        line_width = 2,
        
    )

    farenheit_fig.title.align = 'center'
    farenheit_fig.title.text_font_size = '1em' 
    farenheit_fig.toolbar_location="above"
    farenheit_fig.toolbar.autohide = True
    farenheit_fig.xaxis.formatter = DatetimeTickFormatter(days="%b %d")

    tooltips = [
        ('Temperature', '@farenheit_temperature'),
        ('Date', '@date{%F}')
    ]
    farenheit_fig.add_tools(HoverTool(tooltips=tooltips, formatters={'@date' : 'datetime'}))

    humidity_fig = figure(width=400, 
                 height=400, 
                 x_axis_type="datetime",
                 )

    humidity_fig.line(
        source = chart_data,
        x='date',
        y='humidity',
        line_width = 2,
        
    )

    humidity_fig.title.align = 'center'
    humidity_fig.title.text_font_size = '1em' 
    humidity_fig.toolbar_location="above"
    humidity_fig.toolbar.autohide = True
    humidity_fig.xaxis.formatter = DatetimeTickFormatter(days="%b %d")

    tooltips = [
        ('Humidity', '@humidity'),
        ('Date', '@date{%F}')
    ]
    humidity_fig.add_tools(HoverTool(tooltips=tooltips, formatters={'@date' : 'datetime'}))
    
    heatindex_fig = figure(width=400, 
                 height=400, 
                 x_axis_type="datetime",
                 )

    heatindex_fig.line(
        source = chart_data,
        x='date',
        y='farenheit_temperature',
        line_width = 2,
        
    )

    heatindex_fig.title.text_font_size = '1em' 
    heatindex_fig.toolbar_location="above"
    heatindex_fig.title.align = 'center'
    heatindex_fig.toolbar.autohide = True
    heatindex_fig.xaxis.formatter = DatetimeTickFormatter(days="%b %d")

    tooltips = [
        ('Heat Index', '@heatindex'),
        ('Date', '@date{%F}')
    ]
    heatindex_fig.add_tools(HoverTool(tooltips=tooltips, formatters={'@date' : 'datetime'}))

    plots = {'celsius': fig, 'farenheit' : farenheit_fig, 'humidity':humidity_fig, 'heatindex' : heatindex_fig}
    script, div = components(plots)

    data = {
        "temperature_in_celsius" : dataQuerySet.temperature_in_celsius,
        "temperature_in_farenheit" : dataQuerySet.temperature_in_farenheit,
        "humidity" : dataQuerySet.humidity,
        "heatindex" : dataQuerySet.heatindex,
        'script' : script,
        'div' : div,
    }
    if request.htmx:
        return render(request, "update_homepage.html", context=data)
    return render(request, "homepage.html", context=data)

# def update_homepage(request):
#     dataQuerySet = WeatherData.objects.all().last()
#     chart_queryset = WeatherData.objects.all()    

#     temperatures = [item.temperature_in_celsius for item in chart_queryset]
#     farenheit_temperatures = [item.temperature_in_farenheit for item in chart_queryset]
#     dates = [val.timestamp for val in chart_queryset]



#     chart_data = ColumnDataSource(data = dict(temperature = temperatures, date = dates, farenheit_temperature = farenheit_temperatures))
#     fig = figure(width=400, 
#                  height=400, 
#                  x_axis_type="datetime",
#                  )

#     fig.line(
#         source = chart_data,
#         x='date',
#         y='temperature',
#         line_width = 2,
        
#     )

#     fig.title.align = 'center'
#     fig.title.text_font_size = '1em' 
#     fig.toolbar_location="above"
#     fig.toolbar.autohide = True
#     fig.xaxis.formatter = DatetimeTickFormatter(days="%b %d")


#     tooltips = [
#         ('Temperature', '@temperature'),
#         ('Date', '@date{%F}')
#     ]
#     fig.add_tools(HoverTool(tooltips=tooltips, formatters={'@date' : 'datetime'}))
#     # script, div = components(fig)

#     farenheit_fig = figure(width=400, 
#                  height=400, 
#                  x_axis_type="datetime",
#                  )

#     farenheit_fig.line(
#         source = chart_data,
#         x='date',
#         y='farenheit_temperature',
#         line_width = 2,
        
#     )

#     farenheit_fig.title.align = 'center'
#     farenheit_fig.title.text_font_size = '1em' 
#     farenheit_fig.toolbar_location="above"
#     farenheit_fig.toolbar.autohide = True
#     farenheit_fig.xaxis.formatter = DatetimeTickFormatter(days="%b %d")

#     tooltips = [
#         ('Temperature', '@farenheit_temperature'),
#         ('Date', '@date{%F}')
#     ]
#     farenheit_fig.add_tools(HoverTool(tooltips=tooltips, formatters={'@date' : 'datetime'}))
#     plots = {'div1': fig, 'div2' : farenheit_fig}
#     script, div = components(plots)

#     print(div)

#     data = {
#         "temperature_in_celsius" : dataQuerySet.temperature_in_celsius,
#         "temperature_in_farenheit" : dataQuerySet.temperature_in_farenheit,
#         "humidity" : dataQuerySet.humidity,
#         "heatindex" : dataQuerySet.heatindex,
#         'script' : script,
#         'div' : div,
#     }

#     return render(request, "update_homepage.html", context=data)

def draw_celsius_chart(request):
    queryset = WeatherData.objects.all()


    temperatures = [item.temperature_in_celsius for item in queryset]
    dates = [val.timestamp.strftime("%b %d,%Y") for val in queryset]

    fig = px.line(
        x = dates,
        y = temperatures,
        title='Temperature in ℃',
        labels={
            'x': 'Date', 
            'y': 'Temperature',
        }
    )

    fig.update_layout(
        title={
            'font_size': 22,
            'xanchor': 'center',
            'x': 0.5,   
        }
    )

    chart = fig.to_html()



    return render(request, 'charts.html', {'chart': chart})

def draw_farenheit_chart(request):
    queryset = WeatherData.objects.all()


    farenheits = [item.temperature_in_farenheit for item in queryset]
    dates = [val.timestamp.strftime("%b %d,%Y") for val in queryset]

    fig = px.line(
        x = dates,
        y = farenheits,
        title='Temperature in ℉',
        labels={
            'x': 'Date', 
            'y': 'Temperature',
        }
    )

    fig.update_layout(
        title={
            'font_size': 22,
            'xanchor': 'center',
            'x': 0.5,   
        }
    )

    chart = fig.to_html()



    return render(request, 'charts.html', {'chart': chart})

def draw_humidity_chart(request):
    queryset = WeatherData.objects.all()

    humidity = [item.humidity for item in queryset]
    dates = [val.timestamp.strftime("%b %d,%Y") for val in queryset]

    fig = px.line(
        x = dates,
        y = humidity,
        title='Humidity',
        labels={
            'x': 'Date', 
            'y': 'Humidity',
        }
    )

    fig.update_layout(
        title={
            'font_size': 22,
            'xanchor': 'center',
            'x': 0.5,   
        }
    )

    chart = fig.to_html()



    return render(request, 'charts.html', {'chart': chart})

def draw_heatindex_chart(request):
    queryset = WeatherData.objects.all()


    heatindex = [item.heatindex for item in queryset]
    dates = [val.timestamp.strftime("%b %d,%Y") for val in queryset]

    fig = px.line(
        x = dates,
        y = heatindex,
        title='Heat Index',
        labels={
            'x': 'Date', 
            'y': 'Heat Index',
        }
    )

    fig.update_layout(
        title={
            'font_size': 22,
            'xanchor': 'center',
            'x': 0.5,   
        }
    )

    chart = fig.to_html()



    return render(request, 'charts.html', {'chart': chart})

def line_chart(request):
    chart_queryset = WeatherData.objects.all()    

    temperatures = [item.temperature_in_celsius for item in chart_queryset]
    dates = [val.timestamp for val in chart_queryset]


    chart_data = ColumnDataSource(data = dict(temperature = temperatures, date = dates))
    fig = figure(width=400, 
                 height=400, 
                 x_axis_type="datetime",
                 title = "Temperature in ℃")

    fig.line(
        source = chart_data,
        x='date',
        y='temperature',
        line_width = 2,
        
    )



    fig.title.align = 'center'
    fig.title.text_font_size = '1em' 
    fig.toolbar_location="above"
    fig.toolbar.autohide = True
    fig.xaxis.formatter = DatetimeTickFormatter(days="%b %d")


    tooltips = [
        ('Temperature', '@temperature'),
        ('Date', '@date{%F}')
    ]
    fig.add_tools(HoverTool(tooltips=tooltips, formatters={'@date' : 'datetime'}))
    script, div = components(fig)

    context = {
        'script' : script,
        'div' : div,
    }

    return render(request, 'line.html', context)
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
        # print('data:', data.password)
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
        # print('data:', data)
        serializer = UserSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



