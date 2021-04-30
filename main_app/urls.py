from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('postcards/', views.postcards, name='postcards'),
    path('postcards/create/', views.Create_Postcard.as_view(), name='create_postcard'),
    path('calendar/', views.calendar, name='calendar'),
    # path('show_year/<int:display_year>/', views.show_year, name='show_year'),
    path('requests/', views.requests, name='requests'),
    path('info/', views.info, name='info'),
    path('accounts/register/', views.register, name='register'),


    # sample template with EVERYTHING available. Delete when done building pages
    path('koka', views.koka, name='koka'),
    
]

