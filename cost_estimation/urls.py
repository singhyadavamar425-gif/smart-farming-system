from django.urls import path
from . import views

urlpatterns = [
    path("", views.cost_home, name="cost_home"),
    path("estimate/", views.estimate_cost, name="estimate_cost"),
]