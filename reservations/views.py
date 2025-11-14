from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home_view(request):
    return render(request, "reservations/home.html")

@login_required
def my_reservations_view(request):
    return render(request, "reservations/my_reservations.html")