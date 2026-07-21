from django.urls import path
from . import views

app_name = 'live_weather'

urlpatterns = [
    # Agar live_weather me koi view function hai (jaise weather_info), use map kar dein:
    # path('', views.weather_info, name='index'),
]