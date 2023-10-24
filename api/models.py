""" from django.db import models
from django.contrib.auth.models import User


class UserProfileBase(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=30)
    email = models.EmailField()

    class Meta:
        abstract = True


class Teacher(UserProfileBase):
    # Add customer-specific fields
    phone_number = models.CharField(max_length=15)
    address = models.TextField()


class Student(UserProfileBase):
    # Add employee-specific fields
    employee_id = models.CharField(max_length=10)
    job_title = models.CharField(max_length=50)


class RTE(UserProfileBase):
    # Add employee-specific fields
    employee_id = models.CharField(max_length=10)
    job_title = models.CharField(max_length=50)
 """
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

USER_TYPES = (
    ("admin", "Admin"),
    ("teacher", "Teacher"),
    ("student", "Student"),
)


class User(AbstractUser):
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    # related_name attributes to avoid clashes
    groups = models.ManyToManyField(Group, related_name="api_users")
    user_permissions = models.ManyToManyField(Permission, related_name="api_users")


class RTE(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # courses = models.ManyToManyField(Course, related_name="students")


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
