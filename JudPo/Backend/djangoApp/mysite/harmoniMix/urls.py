from django.urls import path
from . import views
urlpatterns = [
    path('', views.landing, name='Landing'),
    path('song/search/', views.initialSearch, name='InitialSearch'),
    path('song/final/', views.finalSearch, name = 'FinalSearch'),
    path('spotChecker/', views.songSpotify, name='SongSpotify'),
    path('error/', views.error, name='Error'),
]