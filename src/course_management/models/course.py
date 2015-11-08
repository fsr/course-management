from django.db import models
from . import schedule, student, subject



class Course(models.Model):
    schedule = models.OneToOneField(schedule.Schedule)
    teacher = models.ForeignKey(student.Student, related_name="teacher")
    participants = models.ManyToManyField(student.Student)
    active = models.BooleanField(default=False)
    subject = models.ForeignKey(subject.Subject)


    def __str__(self):
        return '{sub}'.format(sub=self.subject.name)
