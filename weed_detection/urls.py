from django.urls import path
from . import views

urlpatterns = [
    path("", views.weed_home, name="weed_home"),
    path("predict/", views.predict_weed, name="predict_weed"),
]