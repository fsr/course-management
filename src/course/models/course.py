from markdown import markdown

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from . import schedule, subject

from user.models import Student

from util.html_clean import clean_for_description


ARCHIVE_STATUSES = (
    ('auto', 't'),
    ('never', 'n'),
    ('archived', 'a'),
)


class Course(models.Model):
    schedule = models.OneToOneField(schedule.Schedule)
    teacher = models.ManyToManyField(Student, related_name="teacher")
    participants = models.ManyToManyField(Student)
    active = models.BooleanField(default=False)
    subject = models.ForeignKey(subject.Subject)
    max_participants = models.IntegerField()
    description = models.TextField(default="No description provided for this course.")
    archiving = models.CharField(max_length=1, choices=ARCHIVE_STATUSES)

    def __str__(self):
        return self.subject.name

    def is_participant(self, student):
        if isinstance(student, User):
            student = student.student
        elif not isinstance(student, Student):
            raise TypeError('Expected {} or {} instance, got {}', Student, User, type(student))

        return self.participants.filter(id=student.id).exists()

    @property
    def joinable(self):
        """
        Returns whether this course can currently be joined.
        """
        (curr, max) = self.saturation_level
        return curr <= max and self.active

    @property
    def saturation_level(self):
        """
        Returns the ratio of currently enrolled participants to maximum allowed
        participants.
        """
        return self.participants.count(), self.max_participants

    def get_description_as_html(self):
        return clean_for_description(markdown(self.description))

    def is_teacher(self, user):
        if isinstance(user, User):
            user = user.student
        elif not isinstance(user, Student):
            raise TypeError('Expected {} or {} instance, got {}', Student, User, type(user))
        return self.teacher.filter(id=user.id).exists()

    def get_distinct_locations(self):
        return self.schedule.slots.values_list('location', flat=True).distinct()

    def as_context(self, student=None):

        participants_count, max_participants = self.saturation_level
        sub_name = self.subject.name
        context = {
            'title': sub_name,
            'course_id': self.id,
            'course': self,
            'backurl': reverse('subject', args=[sub_name]),
            'participants_count': participants_count,
            'max_participants': max_participants,
            'course_is_active': self.active,
        }
        if isinstance(student, Student):
            context['is_subbed'] = student.course_set.filter(id=self.id).exists()

            if self.is_teacher(student):
                context['is_teacher'] = True
                context['students'] = self.participants.all()

        return context

    def can_be_archived(self):
        return self.archiving == 't'

    def is_archived(self):
        return self.archiving == 'a'


class Notification(models.Model):
    subject = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ManyToManyField(Student)
