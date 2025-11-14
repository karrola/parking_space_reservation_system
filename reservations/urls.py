from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home_view, name="home"),
    path("my-reservations/", views.my_reservations_view, name="my_reservations")
]