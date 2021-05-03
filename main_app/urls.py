from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('postcards/', views.postcards, name='postcards'),
    path('postcards/<int:postcard_id>/', views.postcards_detail, name='detail'),
    path('postcards/create/', views.Create_Postcard.as_view(), name='create_postcard'),
    path('postcards/<int:postcard_id>/add_photo/', views.add_photo, name='add_photo'),
    path('calendar/', views.calendar, name='calendar'),
    path('requests/', views.requests, name='requests'),
    path('info/', views.info, name='info'),
    path('accounts/register/', views.register, name='register'),
    

    # sample template with EVERYTHING available. Delete when done building pages
    path('koka', views.koka, name='koka'),
    
]

