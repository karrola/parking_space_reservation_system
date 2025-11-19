from django.db import models

from django.conf import settings

# Create your models here.

# model miejsca parkingowego
class ParkingSpace(models.Model):
    name = models.CharField(max_length=4)

    def __str__(self):
        return self.name

# model rezerwacji
class Reservation(models.Model):
    date_start = models.DateField()
    date_end = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    parking_space = models.ForeignKey(ParkingSpace, on_delete=models.CASCADE, related_name='reservations')
    number_plate = models.CharField(max_length=12)

    def __str__(self):
        return f"Rezerwacja #{self.id}"
