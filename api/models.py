from django.db import models
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
