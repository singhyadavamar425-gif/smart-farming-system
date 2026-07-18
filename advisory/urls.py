from django.urls import path
from . import views

urlpatterns = [
    path("", views.advisory_home, name="advisory_home"),
]