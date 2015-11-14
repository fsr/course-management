from django.db import models
from markdown import markdown

from util.html_clean import clean_for_description
from . import schedule, subject
from django.contrib.auth.models import User
from user.models import Student


class Course(models.Model):
    schedule = models.OneToOneField(schedule.Schedule)
    teacher = models.ManyToManyField(Student, related_name="teacher")
    participants = models.ManyToManyField(Student)
    active = models.BooleanField(default=False)
    subject = models.ForeignKey(subject.Subject)
    max_participants = models.IntegerField()
    description = models.TextField(default="No description provided for this course.")

    def __str__(self):
        return self.subject.name

    @property
    def saturation_level(self):
        return self.participants.count(), self.max_participants

    def get_description_as_html(self):
        return clean_for_description(markdown(self.description))

    def is_teacher(self, user):
        if isinstance(user, User):
            user = user.student
        elif not isinstance(user, Student):
            return False
        return self.teacher.filter(id=user.id).exists()

    def get_distinct_locations(self):
        return self.schedule.slots.values_list('location', flat=True).distinct()
