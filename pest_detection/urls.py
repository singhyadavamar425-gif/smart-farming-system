from django.urls import path
from . import views

urlpatterns = [
    path("", views.pest_home, name="pest_home"),
    path("predict/", views.predict_pest, name="predict_pest"),
]