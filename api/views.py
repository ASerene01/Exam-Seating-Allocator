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
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
User = get_user_model()


def is_admin(user):
    return user.groups.filter(name="RTEs").exists()


def is_student(user):
    return user.groups.filter(name="Students").exists()


def is_teacher(user):
    return user.groups.filter(name="Teachers").exists()


def login_page(request):
    user = request.user
    if user.is_authenticated:
        if user.user_type == "admin":
            return redirect("admin_home/")
        elif user.user_type == "student":
            return redirect("student_home/")
        elif user.user_type == "teacher":
            return redirect("teacher_home/")
    else:
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
    context = {"homeurl": "login_page"}
    return render(request, "login.html", context)


@login_required(login_url="login_page")
@user_passes_test(is_admin, login_url="login_page")
def admin_home(request):
    current_user = request.user
    queryset = User.objects.exclude(id=current_user.id)
    context = {
        "AllUsers": queryset,
        "homeurl": "admin_home",
        "style": "admin_home",
    }
    return render(request, "adminHome.html", context)


@login_required(login_url="login_page")
@user_passes_test(is_student, login_url="login_page")
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
@user_passes_test(is_teacher, login_url="login_page")
def teacher_home(request):
    context = {"homeurl": "student_home"}
    return render(request, "teacherHome.html", context)


@login_required(login_url="login_page")
@user_passes_test(is_admin, login_url="login_page")
def admin_view_profile(request):

    context = {
        "homeurl": "admin_home",
        "style": "admin_home",
    }
    return render(request, "adminViewProfile.html", context)


@user_passes_test(is_admin, login_url="login_page")
def view_users(request):
    users = User.objects.all()
    context = {
        "homeurl": "admin_home",
        "users": users,
        "page_url": "user",
        "style": "view_users",
    }
    return render(request, "viewUsers.html", context)


@user_passes_test(is_admin, login_url="login_page")
def register_user(request):
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
            return redirect("/register_user/")
        useremail = User.objects.filter(email=email)
        if useremail.exists():
            messages.info(request, "Email already registered")
            return redirect("/register_user/")
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
            # Create a Student instance and associate it with the user
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
        return redirect("/view_users/")
    querysetcourse = Course.objects.all()
    context = {
        "style": "registeruser",
        "jslink": "registeruser",
        "Courses": querysetcourse,
        "homeurl": "admin_home",
        "page_url": "user",
    }
    return render(request, "registerUser.html", context)


def logout_page(request):
    logout(request)
    return redirect("login_page")


@login_required(login_url="login_page")
@user_passes_test(is_admin, login_url="login_page")
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
            return redirect("/update_user/" + str(id))
        userdetails.username = username
        exclude_email = User.objects.exclude(email=userdetails.email)
        email_check = exclude_email.filter(email=email)
        if email_check.exists():
            messages.info(request, "Email already registered")
            return redirect("/update_user/" + str(id))
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
        return redirect("view_users")
    context = {
        "homeurl": "admin_home",
        "page_url": "user",
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
@user_passes_test(is_admin, login_url="login_page")
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
    return redirect("view_users")


@user_passes_test(is_admin, login_url="login_page")
def view_courses(request):
    courses = Course.objects.all()
    context = {
        "homeurl": "admin_home",
        "Courses": courses,
        "page_url": "course",
        "style": "view_courses",
    }
    return render(request, "viewCourses.html", context)


@user_passes_test(is_admin, login_url="login_page")
def register_course(request):
    if request.method == "POST":
        data = request.POST
        course = data.get("course").lower()
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
        return redirect("/view_courses/")
    queryset = Course.objects.all()
    context = {
        "homeurl": "admin_home",
        "Courses": queryset,
        "page_url": "course",
    }
    return render(request, "courseRegister.html", context)


@login_required(login_url="login_page")
@user_passes_test(is_admin, login_url="login_page")
def deletecourse(request, id):
    queryset = Course.objects.get(id=id)
    queryset.delete()
    return redirect("view_courses")


@login_required(login_url="login_page")
@user_passes_test(is_admin, login_url="login_page")
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
        "page_url": "course",
    }
    return render(request, "courseUpdate.html", context)


@login_required(login_url="login_page")
@user_passes_test(is_admin, login_url="login_page")
def registerhall(request):
    hallAll = Hall.objects.all()
    if request.method == "POST":
        data = request.POST
        hall_name = data.get("hallname")
        rows = data.get("rows")
        columns = data.get("columns")
        seats = data.get("seats")
        halls = Hall.objects.filter(name=hall_name)
        if halls.exists():
            messages.info(request, "Hall already registered")
            return redirect("/register_hall/")
        hall = Hall.objects.create(
            name=hall_name, rows=rows, columns=columns, noOfSeats=seats
        )
        hall.save()
        # Create seats associated with the hall
        for row in range(int(hall.rows)):
            HallRowSpaces.objects.create(hall=hall, rowAfter=row)
            for column in range(int(hall.columns)):
                Seat.objects.create(hall=hall, row=row, column=column)
        for column in range(int(hall.columns)):
            HallColumnSpaces.objects.create(hall=hall, columnAfter=column)

        return redirect("/edit_hall_layout/" + hall_name)
    context = {
        "style": "registerhall",
        "jslink": "registerhall",
        "homeurl": "admin_home",
        "page_url": "hall",
        "halls": hallAll,
    }
    return render(request, "registerHall.html", context)


@user_passes_test(is_admin, login_url="login_page")
def deletehall(request, id):
    queryset = Hall.objects.get(id=id)
    queryset.delete()
    return redirect("register_hall")


@user_passes_test(is_admin, login_url="login_page")
def edithalllayout(request, name):
    hall = Hall.objects.get(name=name)
    hallcolumnspaces = hall.columnspaces.all()
    forLastColumn = hallcolumnspaces.order_by("columnAfter")
    lastColumn = forLastColumn.last()
    hallrowspaces = hall.rowspaces.all()
    seatNumbers = hall.seats.all()
    context = {
        "style": "edithall",
        "jslink": "edithall",
        "homeurl": "admin_home",
        "hall": hall,
        "hallRows": range(0, hall.rows),
        "hallColumns": range(0, hall.columns),
        "seatNumbers": seatNumbers,
        "hallColumnSpaces": hallcolumnspaces,
        "lastColumn": lastColumn,
        "hallRowSpaces": hallrowspaces,
    }
    return render(request, "editHall.html", context)


@user_passes_test(is_admin, login_url="login_page")
def viewhalllayout(request, id):
    hall = Hall.objects.get(id=id)
    hallcolumnspaces = hall.columnspaces.all()
    hallrowspaces = hall.rowspaces.all()
    seatNumbers = hall.seats.all()
    context = {
        "style": "view_hall_layout",
        "jslink": "view_hall_layout",
        "homeurl": "admin_home",
        "hall": hall,
        "hallRows": range(0, hall.rows),
        "hallColumns": range(0, hall.columns),
        "seatNumbers": seatNumbers,
        "hallColumnSpaces": hallcolumnspaces,
        "hallRowSpaces": hallrowspaces,
    }
    return render(request, "viewHallLayout.html", context)


@user_passes_test(is_admin, login_url="login_page")
def removeseatfromhall(request, id):
    seatToDelete = Seat.objects.get(id=id)
    hallName = seatToDelete.hall.name
    seatToDelete.is_deleted = True
    seatToDelete.save()
    return redirect("/edit_hall_layout/" + hallName)


@user_passes_test(is_admin, login_url="login_page")
def addseattohall(request, id):
    seatToAdd = Seat.objects.get(id=id)
    hallName = seatToAdd.hall.name
    seatToAdd.is_deleted = False
    seatToAdd.save()
    return redirect("/edit_hall_layout/" + hallName)


@user_passes_test(is_admin, login_url="login_page")
def addcolumnspacetohall(request, id):
    spaceToAdd = HallColumnSpaces.objects.get(id=id)
    hallName = spaceToAdd.hall.name
    spaceToAdd.is_space = True
    spaceToAdd.save()
    return redirect("/edit_hall_layout/" + hallName)


@user_passes_test(is_admin, login_url="login_page")
def removecolumnspacefromhall(request, id):
    spaceToRemove = HallColumnSpaces.objects.get(id=id)
    hallName = spaceToRemove.hall.name
    spaceToRemove.is_space = False
    spaceToRemove.save()
    return redirect("/edit_hall_layout/" + hallName)


@user_passes_test(is_admin, login_url="login_page")
def addrowspacetohall(request, id):
    spaceToAdd = HallRowSpaces.objects.get(id=id)
    hallName = spaceToAdd.hall.name
    spaceToAdd.is_space = True
    spaceToAdd.save()
    return redirect("/edit_hall_layout/" + hallName)


@user_passes_test(is_admin, login_url="login_page")
def removerowspacefromhall(request, id):
    spaceToRemove = HallRowSpaces.objects.get(id=id)
    hallName = spaceToRemove.hall.name
    spaceToRemove.is_space = False
    spaceToRemove.save()
    return redirect("/edit_hall_layout/" + hallName)


from .forms import EventForm


def admin_events_view(request):
    events = Event.objects.all()
    context = {"homeurl": "admin_home", "events": events}
    return render(request, "viewEvents.html", context)


def create_new_event(request):
    if request.method == "POST":
        data = request.POST
        name = data.get("event")
        date = data.get("Date")
        startTime = data.get("startTime")
        endTime = data.get("endTime")
        eventCheck = Event.objects.filter(
            date=date, start_time=startTime, end_time=endTime
        )
        if eventCheck.exists():
            messages.info(request, "Event Already There ")
            return redirect("/create_new_event/")
        event = Event.objects.create(
            name=name, date=date, start_time=startTime, end_time=endTime
        )
        event.save()
        id = event.id
        return redirect("/create_new_event_courses/" + str(id))

    context = {"homeurl": "admin_home", "style": "create_new_event"}
    return render(request, "createNewEvent.html", context)


def create_new_event_courses(request, id):
    courses = Course.objects.all()
    if request.method == "POST":
        data = request.POST
        selectedCourses = data.getlist("selectedcourses")
        for eachcourse in selectedCourses:
            course = Course.objects.get(id=eachcourse)
            event = Event.objects.get(id=id)
            EventCourses.objects.create(event=event, course=course)
        return redirect("/create_new_event_halls/" + id)
    context = {"homeurl": "admin_home", "courses": courses}
    return render(request, "createNewEventCourses.html", context)


# After the hall creation allocation will be done in this page
def create_new_event_halls(request, id):
    halls = Hall.objects.all()
    if request.method == "POST":
        data = request.POST
        selectedHalls = data.getlist("selectedhalls")
        event = Event.objects.get(id=id)
        for eachHall in selectedHalls:
            hall = Hall.objects.get(id=eachHall)
            EventHalls.objects.create(event=event, hall=hall)
        eligible = allocation(id)
        print(eligible)
        if eligible == False:
            messages.error(request, "Not enough seats for all students")
            return redirect("/create_new_event_halls/" + id)
        return redirect("/admin_view_event_info/" + id)
    context = {"homeurl": "admin_home", "halls": halls}
    return render(request, "createNewEventHalls.html", context)


@user_passes_test(is_admin, login_url="login_page")
def delete_event(request, id):
    event = Event.objects.get(id=id)
    deleted = event.delete()
    if deleted:
        messages.success(request, "Event " + event.name + " has been deleted")

    else:
        messages.error(request, "Event was not deleted ")
    return redirect("admin_events_view")


@user_passes_test(is_admin, login_url="login_page")
def admin_view_event_info(request, id):
    event = Event.objects.get(id=id)
    event_halls = event.eventhall.all()
    hall = event_halls.first().hall
    allocations = event.eventallocation.all()
    seats = []
    students = []
    for allocation in allocations:
        seats.append(allocation.seat)
        students.append(allocation.student)

    hallcolumns = hall.columnspaces.all()
    hallrows = hall.rowspaces.all()
    seatNumbers = hall.seats.all()
    context = {
        "style": "view_hall_layout",
        "jslink": "view_hall_layout",
        "homeurl": "admin_home",
        "seatNumbers": seatNumbers,
        "hallColumns": hallcolumns,
        "hallRows": hallrows,
        "allocationSeats": seats,
    }
    return render(request, "adminViewEventInfo.html", context)


def allocation(id):

    event = Event.objects.get(id=id)
    event_courses = event.eventcourse.all()
    event_halls = event.eventhall.all()
    if event_courses.count() == 1:

        course = event_courses.first().course
        students = course.students.all()

        # Check all the selected halls for eligibility
        countStudents = students.count()

        """ if hallCount > 1:
            hall = event_halls.first().hall
            seats = hall.seats.filter(is_deleted=False)
            countSeats = 0
            for seat in seats:
                if seat.column % 2 == 0:
                    countSeats = countSeats + 1

            countSeats = int(seats.count())
            if countSeats < countStudents:
                event.eventhall.all().delete()
                return False
            for student in students:
                for seat in seats:
                    if seat.column % 2 == 0:
                        check = Allocation.objects.filter(event=event, seat=seat)

                        if not check.exists():
                            Allocation.objects.create(
                                event=event, seat=seat, student=student
                            )

                            break
        elif hallCount == 1: """
        countSeats = 0
        neededSeats = []
        for event_hall in event_halls:

            hall = event_hall.hall
            seats = hall.seats.exclude(is_deleted=True)

            for seat in seats:
                if seat.column % 2 == 0:
                    countSeats = countSeats + 1
            print(countSeats)
        if countSeats < countStudents:
            event.eventhall.all().delete()
            return False

        for event_hall in event_halls:
            hall = event_hall.hall
            seats = hall.seats.exclude(is_deleted=True)
            countSeats = 0
            for seat in seats:
                if seat.column % 2 == 0:
                    countSeats = countSeats + 1
            lastSeatCheck = 0
            for student in students:
                if lastSeatCheck == countSeats:
                    break
                for seat in seats:
                    if seat.column % 2 == 0:
                        check = Allocation.objects.filter(event=event, seat=seat)
                        allocated = Allocation.objects.filter(
                            event=event, student=student
                        )
                        if not check.exists() and not allocated.exists():
                            Allocation.objects.create(
                                event=event, seat=seat, student=student
                            )
                            lastSeatCheck = lastSeatCheck + 1
                            break
        return True
    elif event_courses.count() == 2:
        countStudents = 0
        for event_course in event_courses:
            course = event_course.course
            students = course.students.all()
            countStudents = countStudents + students.count()
        event_halls = event.eventhall.all()
        hall = event_halls.first().hall
        countSeats = 0
        neededSeats = []
        for event_hall in event_halls:

            hall = event_hall.hall
            seats = hall.seats.exclude(is_deleted=True)

            for seat in seats:
                if seat.column % 2 == 0:
                    countSeats = countSeats + 1
            print(countSeats)
        if countSeats < countStudents:
            event.eventhall.all().delete()
            return False

        for event_hall in event_halls:
            hall = event_hall.hall
            seats = hall.seats.exclude(is_deleted=True)
            countSeats = 0
            lastSeatCheck = 0
            for seat in seats:
                if seat.column % 2 == 0:
                    countSeats = countSeats + 1
            for event_course in event_courses:
                course = event_course.course
                students = course.students.all()
                for student in students:
                    if lastSeatCheck == countSeats:
                        break
                    for seat in seats:
                        if seat.column % 2 == 0:
                            check = Allocation.objects.filter(event=event, seat=seat)
                            allocated = Allocation.objects.filter(
                                event=event, student=student
                            )
                            if not check.exists() and not allocated.exists():
                                Allocation.objects.create(
                                    event=event, seat=seat, student=student
                                )
                                lastSeatCheck = lastSeatCheck + 1
                                break


def demo(request):
    context = {"homeurl": "admin_home", "form": EventForm()}
    return render(request, "demo.html", context)


def get_section(numberofstudents, lastsection):
    if numberofstudents <= 20:
        section = lastsection
    else:
        section = int(lastsection) + 1
        section = str(section)
    return section


# To create a database for checking the system
from faker import Faker

fake = Faker()
import random


URL = "http://127.0.0.1:8000/register_user/"


@user_passes_test(is_admin, login_url="login_page")
def seed_students(request):
    try:
        for _ in range(20):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()
            separator = "@"
            username = email.split(separator, 1)[0]
            password = "student"
            allYear = ["first", "second", "third"]
            allSemester = ["first", "second"]
            fieldofstudy = "computing"
            year = "first"
            semester = "first"
            courses = Course.objects.filter(
                fieldofstudy=fieldofstudy, year=year, semester=semester
            )
            user_image = None
            if user_image is None:
                user_image = "Users/default.jpg"
            user = User.objects.filter(username=username)
            if user.exists():
                messages.info(request, "Username already registered")
                request.POST.field1 = {
                    "value": first_name,
                }
                return redirect("/register_user/")
            useremail = User.objects.filter(email=email)
            if useremail.exists():
                messages.info(request, "Email already registered")
                return redirect("/register_user/")
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                user_type="student",
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
            else:
                # Handle the case where there are no distinct sections
                lastsection = 1
                numberofstudents = 0

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

            messages.info(request, "Successfully registered")
    except Exception as e:
        print(e)
    return redirect("view_users")


@user_passes_test(is_admin, login_url="login_page")
def seed_courses(request):
    try:
        courses = [
            ["Logic and Problem Solving", "Computing", "First", "First"],
            ["Programming", "Computing", "First", "First"],
            [
                "Computer Hardware and Software Architectures",
                "Computing",
                "First",
                "First",
            ],
            ["Introduction to Information Systems", "Computing", "First", "First"],
            ["Logic and Problem Solving", "Computing", "First", "Second"],
            ["Programming", "Computing", "First", "Second"],
            [
                "Computer Hardware and Software Architectures",
                "Computing",
                "First",
                "Second",
            ],
            ["Fundamentals of Computing", "Computing", "First", "Second"],
            ["Software Engineering", "Computing", "Second", "First"],
            ["Databases", "Computing", "Second", "First"],
            [
                "Cloud Computing and the Internet of Things",
                "Computing",
                "Second",
                "First",
            ],
            ["Network Operating Systems", "Computing", "Second", "First"],
            ["Smart Data Discovery", "Computing", "Second", "Second"],
            [
                "Professional Issues, Ethics and Computer Law",
                "Computing",
                "Second",
                "Second",
            ],
            [
                "Advanced Programming and Technologies",
                "Computing",
                "Second",
                "Second",
            ],
            ["Artificial Intelligence", "Computing", "Third", "First"],
            [
                "Advanced Database Systems Development",
                "Computing",
                "Third",
                "First",
            ],
            ["Application Development", "Computing", "Third", "First"],
            ["Project", "Computing", "Third", "First"],
            ["Work Related Learning II", "Computing", "Third", "Second"],
            ["Project", "Computing", "Third", "Second"],
            [
                "Advanced Database Systems Development",
                "Computing",
                "Third",
                "Second",
            ],
            ["Application Development", "Computing", "Third", "Second"],
        ]
        for each in courses:

            course_create = Course.objects.create(
                name=each[0].lower(),
                fieldofstudy=each[1].lower(),
                year=each[2].lower(),
                semester=each[3].lower(),
            )

    except Exception as e:
        print(e)
    return redirect("view_courses")
