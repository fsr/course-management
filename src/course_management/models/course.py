from django.db import models
from . import schedule, student



class Course(models.Model):
    schedule = models.OneToOneField(schedule.Schedule)
    teacher = models.ForeignKey(student.Student, related_name="teacher")
    participants = models.ManyToManyField(student.Student)
    active = models.BooleanField(default=False)
