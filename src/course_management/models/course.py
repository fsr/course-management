from django.db import models
from . import schedule, student, subject


class Course(models.Model):
    schedule = models.OneToOneField(schedule.Schedule)
    teacher = models.ManyToManyField(student.Student, related_name="teacher")
    participants = models.ManyToManyField(student.Student)
    active = models.BooleanField(default=False)
    subject = models.ForeignKey(subject.Subject)
    max_participants = models.IntegerField()
    description = models.TextField(default="No description provided for this course.")

    def __str__(self):
        return '{sub}'.format(sub=self.subject.name)
