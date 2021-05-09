from django.contrib import admin
from .models import Week, Postcard, Photo, Request, Agree

# Register your models here.
admin.site.register(Week)
admin.site.register(Postcard)
admin.site.register(Photo)
admin.site.register(Request)
admin.site.register(Agree)