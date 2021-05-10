from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('postcards/', views.postcards, name='postcards'),
    path('postcards/<int:postcard_id>/', views.postcards_detail, name='detail'),
    path('postcards/create/', views.Create_Postcard.as_view(), name='create_postcard'),
    path('postcards/<int:pk>/edit/', views.Update_Postcard.as_view(), name='update_postcard'),
    path('postcards/<int:pk>/delete/', views.Delete_Postcard.as_view(), name='delete_postcard'),
    path('postcards/<int:postcard_id>/add_photo/', views.add_photo, name='add_photo'),
    path('calendar/', views.calendar, name='calendar'),
    path('calendar/<int:week_id>/propose_swap/', views.propose_swap, name='propose_swap'),
    # path('swaps/update/', views.Update_Swap.as_view(), name='update_swap'),
    path('requests/', views.requests, name='requests'),
    path('requests/<int:request_id>/', views.requests_detail, name='detail'),
    path('requests/<int:request_id>/flip_is_done', views.request_flip_is_done, name='request_flip_is_done'),
    path('requests/create/', views.Create_Request.as_view(), name='create_request'),
    path('requests/<int:pk>/edit/', views.Update_Request.as_view(), name='update_request'),
    path('hide_completed_requests/', views.hide_completed_requests, name='hide_completed_requests'),
    path('info/', views.info, name='info'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/pending/', views.pending, name='pending'),
    path('accounts/<int:pending_user_id>/approve/', views.approve_user, name='approve_user'),
    path('oauth2callback', views.oauth2callback, name='oauth2callback'),

]

