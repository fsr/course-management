from django.db import models
from . import schedule, student



class Course(models.Model):
    schedule = models.OneToOneField(schedule.Schedule)
    teacher = models.ForeighnKey(student.Student)
    participants = models.ManyToManyField(student.Student)
