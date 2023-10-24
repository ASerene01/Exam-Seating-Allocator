from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

User = get_user_model()
from django.shortcuts import render, redirect
from .models import *


# Create your views here.
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username")
            return redirect("login_page")
        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid Password")
            return redirect("login_page")
        else:
            login(request, user)
            return redirect("admin/")

    return render(request, "login.html")
