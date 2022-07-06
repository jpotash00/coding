from django.urls import path
from . import views
urlpatterns = [
    path("songs/", views.songs, name = "songs"),
    path("tester/", views.tester, name = "tester"),
    path("", views.home, name = "home")
]