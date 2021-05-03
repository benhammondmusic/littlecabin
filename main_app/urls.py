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
    path('requests/<int:request_id>/', views.requests_detail, name='detail'),
    path('requests/<int:request_id>/flip_is_done', views.request_flip_is_done, name='request_flip_is_done'),
    path('requests/create/', views.Create_Request.as_view(), name='create_request'),
    path('info/', views.info, name='info'),
    path('accounts/register/', views.register, name='register'),

]

