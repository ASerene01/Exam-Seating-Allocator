from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

USER_TYPES = (
    ("admin", "Admin"),
    ("teacher", "Teacher"),
    ("student", "Student"),
)
FIELDOFSTUDY = (
    ("computing", "Computing"),
    ("networking", "Networking"),
    ("multimedia", "Multimedia"),
)
YEAR = (
    ("first", "First"),
    ("second", "Second"),
    ("third", "Third"),
)

SEMESTER = (
    ("first", "First"),
    ("econd", "Second"),
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
    fieldofstudy = models.CharField(
        max_length=20, choices=FIELDOFSTUDY, default="computing"
    )
    year = models.CharField(max_length=20, choices=YEAR, default="first")
    semester = models.CharField(max_length=20, choices=SEMESTER, default="first")


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fieldofstudy = models.CharField(
        max_length=20, choices=FIELDOFSTUDY, default="computing"
    )
    year = models.CharField(max_length=20, choices=YEAR, default="first")
    semester = models.CharField(max_length=20, choices=SEMESTER, default="first")
    courses = models.ManyToManyField(Course, related_name="students")
    section = models.CharField(max_length=20, blank=True)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Hall(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    columns = models.IntegerField()
    noOfSeats = models.IntegerField(default=1)


class Seat(models.Model):
    hall = models.ForeignKey(
        Hall, on_delete=models.CASCADE, related_name="seats", blank=True
    )
    row = models.IntegerField()
    column = models.IntegerField()
    is_deleted = models.BooleanField(default=False)


class HallSpaces(models.Model):
    hall = models.ForeignKey(
        Hall, on_delete=models.CASCADE, related_name="spaces", blank=True
    )
    columnAfter = models.IntegerField(blank=True)
    is_space = models.BooleanField(default=False)


""" 
class Event(models.Model):
    date = models.DateField()
    courses = models.ManyToManyField(Course)



class Allocation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    seat = models.OneToOneField(Seat, on_delete=models.SET_NULL, null=True, blank=True)
 """
