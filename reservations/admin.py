from django.contrib import admin

from .models import Reservation, ParkingSpace

# Register your models here.


# rejestracja Reservation w django admin
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("parking_space", "number_plate", "date_start", "time_start", "date_end", "time_end", "user")
    search_fields = ("parking_space", "number_plate", "date_start", "time_start", "date_end", "time_end", "user")
    ordering = ("parking_space",)

admin.site.register(Reservation, ReservationAdmin)

# rejestracja ParkingSpace w django admin
class ParkingSpaceAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)

admin.site.register(ParkingSpace, ParkingSpaceAdmin)


