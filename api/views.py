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
    current_user = request.user
    queryset = User.objects.exclude(id=current_user.id)
    context = {"AllUsers": queryset, "homeurl": "admin_home"}
    return render(request, "adminHome.html", context)


@login_required(login_url="login_page")
def admin_view_profile(request):
    context = {
        "homeurl": "admin_home",
    }
    return render(request, "adminViewProfile.html", context)


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
        courses = Course.objects.filter(
            fieldofstudy=fieldofstudy, year=year, semester=semester
        )

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
        students = Student.objects.filter(
            fieldofstudy=fieldofstudy, year=year, semester=semester
        )
        allsections = students.values("section").distinct()
        if allsections.exists():
            lastsection = allsections.last()["section"]
            lastsectionstudents = Student.objects.filter(section=lastsection)
            numberofstudents = lastsectionstudents.count()
        else:
            # Handle the case where there are no distinct sections
            lastsection = 1
            numberofstudents = 0

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
                section=get_section(numberofstudents, lastsection),
            )
            for course in courses:
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
    context = {
        "style": "register",
        "jslink": "register",
        "Courses": querysetcourse,
        "homeurl": "admin_home",
    }
    return render(request, "register.html", context)


def logout_page(request):
    logout(request)
    return redirect("login_page")


@login_required(login_url="login_page")
def update_user(request, id):
    userdetails = User.objects.get(id=id)
    allCourses = Course.objects.all()
    if userdetails.user_type == "student":
        studentdetails = Student.objects.get(user=userdetails)
        courses = studentdetails.courses.all()
        students = Student.objects.filter(
            fieldofstudy=studentdetails.fieldofstudy,
            year=studentdetails.year,
            semester=studentdetails.semester,
        )
        sections = students.values("section").distinct()
        sections = sections.exclude(section=studentdetails.section)
    else:
        studentdetails = None
        courses = None
        sections = None

    if request.method == "POST":
        data = request.POST
        first_name = data.get("firstname")
        last_name = data.get("lastname")
        username = data.get("username")
        email = data.get("email")
        user_type = (data.get("user_type")).lower()
        password = data.get("password")
        user_image = request.FILES.get("user_image")

        userdetails.first_name = first_name
        userdetails.last_name = last_name
        exclude_username = User.objects.exclude(username=userdetails.username)
        username_check = exclude_username.filter(username=username)
        if username_check.exists():
            messages.info(request, "Username already registered")
            return redirect("/register/")
        userdetails.username = username
        exclude_email = User.objects.exclude(email=userdetails.email)
        email_check = exclude_email.filter(email=email)
        if email_check.exists():
            messages.info(request, "Email already registered")
            return redirect("/register/")
        userdetails.email = email
        userdetails.user_type = user_type
        if user_image is not None:
            userdetails.user_image = user_image
        userdetails.save()
        if password is not None:
            userdetails.set_password(password)
        if user_type == "student":
            fieldofstudy = (data.get("fieldofstudy")).lower()
            year = (data.get("year")).lower()
            semester = (data.get("semester")).lower()
            section = data.get("section")
            if (
                studentdetails.fieldofstudy is not fieldofstudy
                or studentdetails.year is not year
                or studentdetails.semester is not semester
            ):
                studentdetails.courses.clear()
                courses = Course.objects.filter(
                    fieldofstudy=fieldofstudy, year=year, semester=semester
                )
                for course in courses:
                    studentdetails.courses.add(course)

                studentsfilter = Student.objects.filter(
                    fieldofstudy=fieldofstudy, year=year, semester=semester
                )
                allsections = studentsfilter.values("section").distinct()
                if allsections.exists():
                    lastsection = allsections.last()["section"]
                    lastsectionstudents = Student.objects.filter(section=lastsection)
                    numberofstudents = lastsectionstudents.count()
                else:
                    # Handle the case where there are no distinct sections
                    lastsection = 1
                    numberofstudents = 0
                studentdetails.section = get_section(numberofstudents, lastsection)
            else:
                studentdetails.section = section

            studentdetails.fieldofstudy = fieldofstudy
            studentdetails.year = year
            studentdetails.semester = semester

            studentdetails.save()
        return redirect("admin_home")
    context = {
        "homeurl": "admin_home",
        "userdetails": userdetails,
        "studentdetails": studentdetails,
        "studentcourses": courses,
        "allCourses": allCourses,
        "sections": sections,
        "style": "updateuser",
        "jslink": "updateuser",
    }
    return render(request, "adminUpdataUsers.html", context)


@login_required(login_url="login_page")
def deleteuser(request, id):
    queryset = User.objects.get(id=id)
    image_path = queryset.user_image.url

    new_image = image_path.replace("/media/", "/")
    media_root = settings.MEDIA_ROOT
    to_not_delete = media_root + "\\Users\\default.jpg"
    to_not_delete = to_not_delete.replace("/", "\\")
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
        students = Student.objects.filter(
            fieldofstudy=fieldofstudy, year=year, semester=semester
        )
        for student in students:
            student.courses.add(courseobject)
            # if student.courses is not courseobject:

        messages.info(request, "Course successfully registered")
        return redirect("/admin_home/")
    queryset = Course.objects.all()
    context = {"homeurl": "admin_home", "Courses": queryset}
    return render(request, "courseRegister.html", context)


@login_required(login_url="login_page")
def deletecourse(request, id):
    queryset = Course.objects.get(id=id)
    queryset.delete()
    return redirect("register_course")


@login_required(login_url="login_page")
def updatecourse(request, id):
    coursedetails = Course.objects.get(id=id)
    if request.method == "POST":
        data = request.POST
        name = data.get("course")
        fieldofstudy = data.get("fieldofstudy")
        year = data.get("year")
        semester = data.get("semester")
        coursedetails.name = name
        if (
            coursedetails.fieldofstudy is not fieldofstudy
            or coursedetails.year is not year
            or coursedetails.semester is not semester
        ):
            studentsfilter = Student.objects.filter(
                fieldofstudy=coursedetails.fieldofstudy,
                year=coursedetails.year,
                semester=coursedetails.semester,
            )
            if studentsfilter.exists():
                for student in studentsfilter:
                    student.courses.clear()

            coursedetails.fieldofstudy = fieldofstudy
            coursedetails.year = year.lower()
            coursedetails.semester = semester.lower()
            coursedetails.save()
            coursedetails = Course.objects.get(id=id)
            print()
            coursefilter = Course.objects.filter(
                fieldofstudy=fieldofstudy,
                year=year,
                semester=semester,
            )
            print(fieldofstudy, year, semester)
            studentnew = Student.objects.filter(
                fieldofstudy=fieldofstudy,
                year=year,
                semester=semester,
            )
            if studentnew.exists():
                for student in studentnew:
                    for course in coursefilter:
                        student.courses.add(course)
        else:
            coursedetails.save()
        return redirect("/register_course/")
    context = {
        "homeurl": "admin_home",
        "coursedetails": coursedetails,
    }
    return render(request, "courseUpdate.html", context)


@login_required(login_url="login_page")
def student_home(request):
    user = request.user
    student = Student.objects.get(user=user)
    fieldofstudy = student.fieldofstudy
    year = student.year
    semester = student.semester
    courses = student.courses.all()
    context = {
        "homeurl": "student_home",
        "fieldofstudy": fieldofstudy,
        "year": year,
        "semester": semester,
        "courses": courses,
    }
    return render(request, "studentHome.html", context)


@login_required(login_url="login_page")
def teacher_home(request):
    context = {"homeurl": "student_home"}
    return render(request, "teacherHome.html", context)


def get_section(numberofstudents, lastsection):
    if numberofstudents <= 20:
        section = lastsection
    else:
        section = int(lastsection) + 1
        section = str(section)
    return section
