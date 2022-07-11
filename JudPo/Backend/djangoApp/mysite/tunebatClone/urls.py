from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('category/', views.categorySearch, name='categorySearch'),
    path('category/create/', views.categoryCreated, name='categoryCreated')
]