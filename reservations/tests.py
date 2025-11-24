from django.test import TestCase
from datetime import date, time
from django.contrib.auth import get_user_model
from .models import ParkingSpace, Reservation

User = get_user_model()

class ReservationTableTests(TestCase):
    def setUp(self):
        # użytkownik testowy
        self.user = User.objects.create_user(username="testuser", password="123")
        # miejsce parkingowe
        self.space = ParkingSpace.objects.create(name="A1")
        # istniejąca rezerwacja
        Reservation.objects.create(
            parking_space=self.space,
            date_start=date(2025, 12, 12),
            date_end=date(2025, 12, 16),
            time_start=time(8, 0),
            time_end=time(16, 0),
            user=self.user
        )

    def is_available(self, ds, de, ts, te):
        """True = miejsce dostępne (pokazuje się), False = konflikt"""
        conflicts = Reservation.objects.filter(
            date_start__lte=de,
            date_end__gte=ds,
            time_start__lt=te,
            time_end__gt=ts
        ).values_list('parking_space_id', flat=True)
        return self.space.id not in conflicts

    def test_cases_from_table(self):
        # (data_start_day, data_start_month, data_end_day, data_end_month, godz_start, godz_end, expected)
        tests = [
            # Przypadki całkowicie przed lub po istniejącej rezerwacji → dostępne (True)
            ((11,12,11,12,6,8), True),
            ((11,12,11,12,16,20), True),
            ((11,12,11,12,17,20), True),
            ((10,12,10,12,6,8), True),
            ((10,12,10,12,16,20), True),
            ((10,12,10,12,17,20), True),
            ((16,12,16,12,6,8), True),
            ((16,12,16,12,16,20), True),
            ((16,12,16,12,17,20), True),
            ((18,12,19,12,6,8), True),
            ((18,12,19,12,9,15), True),
            ((18,12,19,12,7,17), True),
            ((18,12,19,12,7,9), True),
            ((18,12,19,12,15,17), True),
            ((18,12,19,12,16,20), True),
            ((18,12,19,12,17,20), True),

            # Wszystkie przypadki, które nakładają się choćby częściowo z istniejącą rezerwacją → niedostępne (False)
            ((11,12,17,12,9,15), False),
            ((11,12,17,12,7,17), False),
            ((11,12,17,12,7,9), False),
            ((11,12,17,12,15,17), False),
            ((11,12,17,12,8,16), False),

            ((10,12,13,12,9,15), False),
            ((10,12,13,12,7,17), False),
            ((10,12,13,12,7,9), False),
            ((10,12,13,12,15,17), False),
            ((10,12,13,12,8,16), False),

            ((13,12,16,12,9,15), False),
            ((13,12,16,12,7,17), False),
            ((13,12,16,12,7,9), False),
            ((13,12,16,12,15,17), False),
            ((13,12,16,12,8,16), False),

            ((13,12,18,12,9,15), False),
            ((13,12,18,12,7,17), False),
            ((13,12,18,12,7,9), False),
            ((13,12,18,12,15,17), False),
            ((13,12,18,12,8,16), False),

            ((10,12,12,12,9,15), False),
            ((10,12,12,12,7,17), False),
            ((10,12,12,12,7,9), False),
            ((10,12,12,12,15,17), False),
            ((10,12,12,12,8,16), False),

            ((16,12,18,12,9,15), False),
            ((16,12,18,12,7,17), False),
            ((16,12,18,12,7,9), False),
            ((16,12,18,12,15,17), False),
            ((16,12,18,12,8,16), False),

            # dokładne pokrycie istniejącej rezerwacji → niedostępne
            ((12,12,16,12,8,16), False),

            # częściowe w środku istniejącej → niedostępne
            ((12,12,16,12,9,15), False),
            ((12,12,16,12,7,17), False),
            ((12,12,16,12,7,9), False),
            ((12,12,16,12,15,17), False),
        ]

        for (ds, ms, de, me, ts, te), expected in tests:
            with self.subTest(f"{ds}.{ms}-{de}.{me} {ts}-{te}"):
                result = self.is_available(
                    date(2025, ms, ds),
                    date(2025, me, de),
                    time(ts, 0),
                    time(te, 0)
                )
                self.assertEqual(result, expected)