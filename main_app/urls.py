from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('postcards', views.postcards, name='postcards'),
    path('calendar', views.calendar, name='calendar'),
    path('requests', views.requests, name='requests'),
    path('info', views.info, name='info'),
    path('accounts/register/', views.register, name='register'),


    # sample template with EVERYTHING available. Delete when done building pages
    path('koka', views.koka, name='koka'),
    
]

