from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .forms import ReservationChooseDateForm, ReservationChooseSpaceForm
from .models import Reservation, ParkingSpace
from django.utils import timezone
from datetime import datetime

@login_required
@never_cache
def reservation_view(request):
    # krok 1 - wybór daty i godziny rezerwacji
    if request.method == "POST" and request.POST.get("step") == "choose_date":
        date_form = ReservationChooseDateForm(request.POST)
        if date_form.is_valid():
            date_start = date_form.cleaned_data['date_start']
            date_end = date_form.cleaned_data['date_end']
            time_start = date_form.cleaned_data['time_start']
            time_end = date_form.cleaned_data['time_end']

            # wybieramy miejsca które kolidują i wykluczamy je
            conflicts = Reservation.objects.filter(
                cancelled=False,
                date_start__lte=date_end,
                date_end__gte=date_start,
                time_start__lt=time_end,
                time_end__gt=time_start
            ).values_list('parking_space_id', flat=True)

            available_spaces = ParkingSpace.objects.exclude(id__in=conflicts)

            # jeśli nie ma wolnych miejsc to nie pokazuj drugiego formularza:
            if not available_spaces:
                # flaga żeby zablokować wchodzenie na stronę braku miejsc przez wpisanie url
                request.session['no_free_space'] = True
                return redirect("reservation_no_free_space")

            # przekazujemy dostępne miejsca i wybraną datę rezerwacji do drugiego formularza
            space_form = ReservationChooseSpaceForm(
                available_spaces=available_spaces,
                initial={
                    'date_start': date_start,
                    'date_end': date_end,
                    'time_start': time_start,
                    'time_end': time_end,
                }
            )

            return render(request, "reservations/reservation_choose_space.html", {
                "form": space_form,
                "available_spaces": available_spaces
            })
        else:
            return render(request, "reservations/reservation_choose_date.html", {"form": date_form})

    # krok 2 - wybór miejsca
    elif request.method == "POST" and request.POST.get("step") == "choose_space":
        space_form = ReservationChooseSpaceForm(request.POST)
        if space_form.is_valid():

            # ponowna walidacja w celu zabezpieczenia dodania drugi raz tego samego miejsca po cofnięciu formularza
            date_start = space_form.cleaned_data['date_start']
            date_end = space_form.cleaned_data['date_end']
            time_start = space_form.cleaned_data['time_start']
            time_end = space_form.cleaned_data['time_end']
            parking_space = space_form.cleaned_data['parking_space']

            conflicts = Reservation.objects.filter(
                cancelled=False,
                parking_space=parking_space,
                date_start__lte=date_end,
                date_end__gte=date_start,
                time_start__lt=time_end,
                time_end__gt=time_start
            ).exists()

            if conflicts:
                space_form.add_error(None, "To miejsce zostało już zarezerwowane.")
                return render(request, "reservations/reservation_choose_space.html", {"form": space_form})
            
            Reservation.objects.create(
                parking_space=space_form.cleaned_data['parking_space'],
                user=request.user,
                date_start=space_form.cleaned_data['date_start'],
                date_end=space_form.cleaned_data['date_end'],
                time_start=space_form.cleaned_data['time_start'],
                time_end=space_form.cleaned_data['time_end'],
                number_plate=space_form.cleaned_data['number_plate'],
            )

            # flaga żeby zablokować wchodzenie na stronę sukcesu przez wpisanie url
            request.session['reservation_done'] = True
            return redirect("reservation_success")
        else:
            return render(request, "reservations/reservation_choose_space.html", {"form": space_form})
   
    # basic get
    else:
        date_form = ReservationChooseDateForm()
        return render(request, "reservations/reservation_choose_date.html", {"form": date_form})

@login_required
def reservation_success_view(request):
    # sprawdzamy czy jest flaga
    if not request.session.get('reservation_done'):
        return redirect("reservation")
    
    # renderujemy i usuwamy flagę
    del request.session['reservation_done']
    return render(request, "reservations/reservation_success.html")

@login_required
def reservation_no_free_space_view(request):
    # sprawdzamy czy jest flaga
    if not request.session.get('no_free_space'):
        return redirect("reservation")
    
    # renderujemy i usuwamy flagę
    del request.session['no_free_space']
    return render(request, "reservations/reservation_no_free_space.html")

@login_required
@never_cache
def my_reservations_view(request):
    user = request.user
    now = timezone.localtime()

    cancelled = user.reservations.filter(cancelled=True)

    active = []
    finished = []
    upcoming = []

    for reservation in user.reservations.filter(cancelled=False):
        end_datetime = timezone.make_aware(
            datetime.combine(reservation.date_end, reservation.time_end)
        )

        start_datetime = timezone.make_aware(
            datetime.combine(reservation.date_start, reservation.time_start)
        )

        if end_datetime < now:
            finished.append(reservation)
        elif start_datetime > now:
            upcoming.append(reservation)
        else:
            active.append(reservation)

    context = {
        "active": active,
        "upcoming": upcoming,
        "finished": finished,
        "cancelled": cancelled,
        "categories": [
            ("Aktywne rezerwacje", active),
            ("Nadchodzące rezerwacje", upcoming),
            ("Zakończone rezerwacje", finished),
            ("Anulowane rezerwacje", cancelled),
        ],
    }

    return render(request, "reservations/my_reservations.html", context)

@login_required
def reservation_cancel_view(request):
    if request.method != "POST":
        return redirect("reservation")
    
    reservation_id = request.POST.get("reservation_id")
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        user=request.user
    )

    reservation.cancelled = True
    reservation.save()

    request.session['reservation_cancelled'] = True
    return redirect("reservation_cancelled")

@login_required
def reservation_cancelled_view(request):
    # sprawdzamy czy jest flaga
    if not request.session.get('reservation_cancelled'):
        return redirect("reservation")
    
    # renderujemy i usuwamy flagę
    del request.session['reservation_cancelled']
    return render(request, "reservations/reservation_cancelled.html")
