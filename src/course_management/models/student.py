from django.db import models
from django.contrib.auth.models import User
from . import faculty


class Student(models.Model):
    user = models.OneToOneField(User)
    s_nummer = models.CharField(max_length=50)
    faculty = models.ForeighnKey(faculty.Faculty)
