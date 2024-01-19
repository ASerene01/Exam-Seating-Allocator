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


admin.site.register(User, UserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(RTE, RTEAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Hall, HallAdmin)
