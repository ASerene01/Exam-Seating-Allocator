from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
import os

User = get_user_model()
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required


# Create your views here.
User = get_user_model()


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username")
            return redirect("login_page")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.error(request, "Success")
            if user.user_type == "admin":
                return redirect("admin_home/")
            elif user.user_type == "student":
                return redirect("student_home/")
            elif user.user_type == "teacher":
                return redirect("teacher_home/")
        else:
            messages.error(request, "Invalid password")

    return render(request, "login.html")


@login_required(login_url="login_page")
def admin_home(request):
    queryset = User.objects.all()
    context = {"AllUsers": queryset, "homeurl": "admin_home"}
    return render(request, "adminHome.html", context)


@login_required(login_url="login_page")
def register(request):
    if request.method == "POST":
        data = request.POST
        first_name = data.get("firstname")
        last_name = data.get("lastname")
        username = data.get("username")
        email = data.get("email")
        user_type = (data.get("user_type")).lower()
        password = data.get("password")
        user_image = request.FILES.get("user_image")

        fieldofstudy = (data.get("fieldofstudy")).lower()
        year = (data.get("year")).lower()
        semester = (data.get("semester")).lower()
        selected_courses = data.getlist("selected_courses")
        if user_image is None:
            user_image = "Users/default.jpg"
        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request, "Username already registered")
            request.POST.field1 = {
                "value": first_name,
            }
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
            user_image=user_image,
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
            student = Student.objects.create(
                user=user,
                fieldofstudy=fieldofstudy,
                year=year,
                semester=semester,
                section="",
            )
            for selected_course in selected_courses:
                course = Course.objects.get(name=selected_course)
                student.courses.add(course)
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
    querysetcourse = Course.objects.all()
    context = {"style": "register", "Courses": querysetcourse}
    return render(request, "register.html", context)


def logout_page(request):
    logout(request)
    return redirect("login_page")


@login_required(login_url="login_page")
def deleteuser(request, id):
    queryset = User.objects.get(id=id)
    image_path = queryset.user_image.url
    to_not_delete = "C:\\Users\\amitb\\OneDrive\\Desktop\\FYP Project\\static\\myapp\\Pictures\\Users\\default.jpg"
    new_image = image_path.replace("/media/", "/")
    media_root = settings.MEDIA_ROOT
    to_delete_path = media_root + new_image
    to_delete_path = to_delete_path.replace("/", "\\")
    for root, dirs, files in os.walk(media_root):
        for file in files:
            file_path = os.path.join(root, file)
            file_path = file_path.replace("/", "\\")
            if to_delete_path == file_path and to_not_delete != to_delete_path:
                print("User Image removed")
                os.remove(file_path)
    queryset.delete()
    messages.info(request, "Successfully Deleted")
    return redirect("admin_home")


@login_required(login_url="login_page")
def register_course(request):
    if request.method == "POST":
        data = request.POST
        course = data.get("course")
        fieldofstudy = (data.get("fieldofstudy")).lower()
        year = (data.get("year")).lower()
        semester = (data.get("semester")).lower()
        coursename = Course.objects.filter(
            name=course, fieldofstudy=fieldofstudy, year=year, semester=semester
        )
        if coursename.exists():
            messages.info(request, "Course already registered")
            return redirect("/register_course/")
        courseobject = Course.objects.create(
            name=course, fieldofstudy=fieldofstudy, year=year, semester=semester
        )
        courseobject.save()

        messages.info(request, "Course successfully registered")
        return redirect("/admin_home/")
    queryset = Course.objects.all()
    context = {"Courses": queryset}
    return render(request, "register_course.html", context)


@login_required(login_url="login_page")
def deletecourse(request, id):
    queryset = Course.objects.get(id=id)
    queryset.delete()
    return redirect("register_course")


def student_home(request):
    context = {"homeurl": "student_home"}
    return render(request, "studentHome.html", context)


def teacher_home(request):
    context = {"homeurl": "student_home"}
    return render(request, "teacherHome.html", context)
