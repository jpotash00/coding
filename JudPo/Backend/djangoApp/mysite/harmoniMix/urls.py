from django.urls import path
from . import views
urlpatterns = [
    path('', views.landing, name='landing'),
    path('songlist/', views.initialSearch, name='initialSearch'),
    # path('songlist/final/', views.finalSearch, name = 'finalSearch'),
    path('category/create/', views.categoryCreated, name='categoryCreated')
]