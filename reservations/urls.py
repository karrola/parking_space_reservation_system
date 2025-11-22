from django.urls import path
from . import views

urlpatterns = [
    path("reservation/", views.reservation_view, name="reservation"),
    path("reservation-success/", views.reservation_success_view, name="reservation_success"),
    path("my-reservations/", views.my_reservations_view, name="my_reservations")
]