from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('koka', views.koka, name='koka'),
    # more routes will go here
]

