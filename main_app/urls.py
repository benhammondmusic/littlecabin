from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('calendar', views.calendar, name='calendar'),


    # sample template with EVERYTHING available. Delete when done building pages
    path('koka', views.koka, name='koka'),
    
]

