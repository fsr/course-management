from django.db import models
from django.contrib.auth.models import User
from . import faculty


class Student(models.Model):
    user = models.OneToOneField(User)
    s_nummer = models.CharField(max_length=50)
    faculty = models.ForeignKey(faculty.Faculty)

    def __str__(self):
        return '{first} {last}'.format(first=self.user.first_name, last=self.user.last_name)
