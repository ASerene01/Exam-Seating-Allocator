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
            if user.user_type == "admin":
                return redirect("admin_home/")
            login(request, user)
            messages.error(request, "Success")
        else:
            messages.error(request, "Invalid password")

    return render(request, "login.html")


def admin_home(request):
    return render(request, "adminHome.html")


def register(request):
    if request.method == "POST":
        data = request.POST
        first_name = data.get("firstname")
        last_name = data.get("lastname")
        username = data.get("username")
        email = data.get("email")
        user_type = (data.get("user_type")).lower()
        password = data.get("password")
        print(user_type)
        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request, "Username already registered")
            return redirect("/register/")
        useremail = User.objects.filter(email=email)
        if useremail.exists():
            messages.info(request, "Email already registered")
            return redirect("/register/")
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            user_type=user_type,
        )
        user.set_password(password)
        user.save()

        if user_type == "admin":
            # Create a Teacher instance and associate it with the user
            rte = RTE.objects.create(user=user)

            # Add the user to a group if needed (e.g., "Teachers" group)
            rte_group, created = Group.objects.get_or_create(name="RTEs")
            user.groups.add(rte_group)

        elif user_type == "student":
            # Create a Teacher instance and associate it with the user
            student = Student.objects.create(user=user)

            # Add the user to a group if needed (e.g., "Teachers" group)
            student_group, created = Group.objects.get_or_create(name="Students")
            user.groups.add(student_group)
        elif user_type == "teacher":
            # Create a Teacher instance and associate it with the user
            teacher = Teacher.objects.create(user=user)

            # Add the user to a group if needed (e.g., "Teachers" group)
            teacher_group, created = Group.objects.get_or_create(name="Teachers")
            user.groups.add(teacher_group)
        messages.info(request, "Successfully registered")
        return redirect("/register/")
    return render(request, "register.html")
