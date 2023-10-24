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
        User = get_user_model()
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username")
            return redirect("login_page")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.error(request, "Success")
        else:
            messages.error(request, "Invalid password")

    return render(request, "login.html")
