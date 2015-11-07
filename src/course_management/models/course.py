from django.db import models
from . import schedule, student



class Course(models.Model):
    schedule = models.OneToOneField(schedule.Schedule)
    teacher = models.ManyToOneField(student.Student)
    participants = models.ManyToMany(student.Student)
