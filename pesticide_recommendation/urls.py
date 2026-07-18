from django.urls import path
from . import views

urlpatterns = [
    path("", views.pesticide_home, name="pesticide_home"),
    path("recommend/", views.recommend_pesticide, name="recommend_pesticide"),
]