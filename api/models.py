from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

USER_TYPES = (
    ("admin", "Admin"),
    ("teacher", "Teacher"),
    ("student", "Student"),
)


class User(AbstractUser):
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    user_image = models.ImageField(
        upload_to="Users",
    )
    # related_name attributes to avoid clashes
    groups = models.ManyToManyField(Group, related_name="api_users")
    user_permissions = models.ManyToManyField(Permission, related_name="api_users")


class RTE(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Course(models.Model):
    name = models.CharField(max_length=100)


class Section(models.Model):
    section_name = models.CharField(max_length=50)
    courses = models.ManyToManyField(Course, related_name="courses_section")


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sections = models.ManyToManyField(Section, related_name="students")


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
