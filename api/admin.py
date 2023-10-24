from django.contrib import admin

# Register your models here.
from .models import Teacher, Student, RTE


class TeacherAdmin(admin.ModelAdmin):
    pass


class StudentAdmin(admin.ModelAdmin):
    list_display = ["user"]


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(RTE)
