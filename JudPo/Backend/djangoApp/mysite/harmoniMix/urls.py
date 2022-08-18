from django.urls import path
from . import views
urlpatterns = [
    path('', views.landing, name='Landing'),
    path('song/search/', views.initialSearch, name='InitialSearch'),
    # path('songlist/final/', views.finalSearch, name = 'finalSearch'),
    path('song/insert/', views.songInserted, name='SongInserted'),
    path('about/', views.about, name = 'About')
]