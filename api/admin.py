from django.contrib import admin

# Register your models here.
from .models import Teacher, Student, RTE


class TeacherAdmin(admin.ModelAdmin):
    list_display = ["username", "email"]


class StudentAdmin(admin.ModelAdmin):
    list_display = ["username", "email"]


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(RTE)
