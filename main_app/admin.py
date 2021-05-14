from django.contrib import admin
from .models import WeatherReport, Week, Postcard, Photo, Request, Agree, Swap

# Register your models here.
admin.site.register(Week)
admin.site.register(Postcard)
admin.site.register(Photo)
admin.site.register(Request)
admin.site.register(Agree)
admin.site.register(Swap)
admin.site.register(WeatherReport)