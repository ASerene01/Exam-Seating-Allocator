from django.contrib import admin
from .models import User
from .models import Teacher, Student, RTE


class TeacherAdmin(admin.ModelAdmin):
    list_display = ["user"]


class StudentAdmin(admin.ModelAdmin):
    list_display = ["user"]


class RTEAdmin(admin.ModelAdmin):
    list_display = ["user"]


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "user_type", "first_name", "last_name", "email")
    # Add 'user_type' to the fields attribute to make it editable in the admin panel
    fields = ("username", "user_type", "first_name", "last_name", "email", "password")


admin.site.register(User, UserAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(RTE, RTEAdmin)
