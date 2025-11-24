from django.urls import path
from . import views

urlpatterns = [
    path("reservation/", views.reservation_view, name="reservation"),
    path("reservation-success/", views.reservation_success_view, name="reservation_success"),
    path("reservation-no-free-space/", views.reservation_no_free_space_view, name="reservation_no_free_space"),
    path("my-reservations/", views.my_reservations_view, name="my_reservations")
]