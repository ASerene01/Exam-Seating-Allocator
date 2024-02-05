from django import forms
from .models import *


courses = Course.objects.all()
courseChoices = [(course.id, course.name) for course in courses]


class EventForm(forms.Form):
    courses = forms.MultipleChoiceField(choices=courseChoices)
    