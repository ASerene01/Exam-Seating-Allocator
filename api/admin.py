from django.contrib import admin
from .models import User
from .models import *


class TeacherAdmin(admin.ModelAdmin):
    list_display = ["user"]


class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "fieldofstudy", "year", "semester")
    fields = ("name", "fieldofstudy", "year", "semester")


class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "fieldofstudy",
        "year",
        "semester",
        "section",
        "display_courses",
    ]

    def display_courses(self, obj):
        return ", ".join([course.name for course in obj.courses.all()])

    display_courses.short_description = "Courses"
    fields = ("user", "fieldofstudy", "year", "semester", "section")


class RTEAdmin(admin.ModelAdmin):
    list_display = ["user"]


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "user_type",
        "first_name",
        "last_name",
        "email",
        "user_image",
    )
    # Add 'user_type' to the fields attribute to make it editable in the admin panel
    fields = (
        "username",
        "user_type",
        "first_name",
        "last_name",
        "email",
        "password",
        "user_image",
    )


class HallAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "rows", "columns")
    fields = ("id", "name", "rows", "columns")


class SeatAdmin(admin.ModelAdmin):
    list_display = ("id", "hall", "row", "column")
    fields = ("id", "hall", "row", "column")


class HallColumnSpaceAdmin(admin.ModelAdmin):
    list_display = ("hall", "columnAfter")
    fields = ("hall", "columnAfter")


class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "start_time", "end_time")
    fields = ("name", "date", "start_time", "end_time")


class EventCoursesAdmin(admin.ModelAdmin):
    list_display = ("event", "course")
    field = ("event", "course")


class EventHallsAdmin(admin.ModelAdmin):
    list_display = ("event", "hall")
    field = ("event", "hall")


class AllocationAdmin(admin.ModelAdmin):
    list_display = ("event", "student", "seat")
    field = ("event", "student", "seat")


admin.site.register(User, UserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(RTE, RTEAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Hall, HallAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(HallColumnSpaces, HallColumnSpaceAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventCourses, EventCoursesAdmin)
admin.site.register(EventHalls, EventHallsAdmin)
admin.site.register(Allocation, AllocationAdmin)
