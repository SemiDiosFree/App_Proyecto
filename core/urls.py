from django.urls import path
from .import views 

core_patterns = [
    path('', views.home, name="home"),
]