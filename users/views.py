from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth import login, logout
from .forms import EmailAuthenticationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def auth_view(request):
    return render(request, "users/auth.html")

def sign_up_view(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect("home")
    else:
        form = UserForm()
    return render(request, "users/sign_up.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home") 
    else:
        form = EmailAuthenticationForm()
    return render(request, "users/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("home")