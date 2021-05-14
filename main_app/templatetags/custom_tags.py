from django import template
from django.urls import reverse
from ..models import WeatherReport
from datetime import datetime, timedelta
from django.utils import timezone

# for Open Weather API
from ..fetch_weather import update_current_weather

register = template.Library()

@register.simple_tag
def anchor(url_name, section_id):
    return reverse(url_name) + '#' + section_id

@register.simple_tag
def current_weather():

    # retrieve weather report from DB
    weather = WeatherReport.objects.first()

    # if no weather in DB, fetch it from API and store to DB as well
    if not weather:
        # print("no stored weather")
        weather_dict = update_current_weather()
        # print("fetching current weather via API") 
        weather = WeatherReport()
        weather.temp = weather_dict["temp"]
        weather.conditions = weather_dict["conditions"]  
        weather.save()   

    # if it exists in DB, use if it's less than 10 minutes old, else refetch from API
    now = timezone.now()
    if now - weather.created > timezone.timedelta(minutes = 10):
        # print("stored weather out of date" )
        weather_dict = update_current_weather()
        # print("refreshing current weather via API") 
        weather = WeatherReport()
        weather.temp = weather_dict["temp"]
        weather.conditions = weather_dict["conditions"]  
        weather.save()  
  

    temp = weather.temp
    conditions = weather.conditions
    # print("TEMP", temp, "CONDITIONS", conditions)

    weather_string = f'{conditions} {temp}'
    return weather_string
