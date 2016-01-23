from markdown import markdown

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from guardian.models import UserObjectPermission

from . import schedule, subject

from user.models import UserInformation, get_user_information

from util.html_clean import clean_for_description

from datetime import date


ARCHIVE_STATUSES = (
    ('t', 'auto'),
    ('n', 'never'),
    ('a', 'archived'),
)


class Course(models.Model):
    schedule = models.OneToOneField(schedule.Schedule)
    teacher = models.ManyToManyField(UserInformation, related_name="teacher")
    participants = models.ManyToManyField(UserInformation)
    active = models.BooleanField(default=False)
    subject = models.ForeignKey(subject.Subject)
    max_participants = models.IntegerField()
    description = models.TextField(blank=True, default="")
    archiving = models.CharField(max_length=1, choices=ARCHIVE_STATUSES)
    queue = models.ManyToManyField(UserInformation, related_name='waiting_for')
    student_only = models.BooleanField(default=False)
    start_time = models.DateField(default=date.today())
    end_time = models.DateField(default=date.today())

    class IsFull(Exception):
        pass

    class IsInactive(Exception):
        pass

    class IsNotEnrolled(Exception):
        pass

    class IsEnrolled(Exception):
        pass

    def __str__(self):
        return self.subject.name

    def enroll(self, student):
        student = get_user_information(student)
        if self._is_participant(student):
            raise self.IsEnrolled
        elif not self.active:
            raise self.IsInactive
        elif self.saturated:
            raise self.IsFull
        else:
            self.participants.add(student)

    def unenroll(self, student):

        student = get_user_information(student)

        if self._is_participant(student):
            self.participants.remove(student)
        else:
            raise self.IsNotEnrolled

    def _is_participant(self, student):
        student = get_user_information(student)
        return student in self.participants.all()

    def is_participant(self, student):
        return self._is_participant(get_user_information(student))

    @property
    def saturated(self):
        (curr, max) = self.saturation_level
        return curr >= max

    @property
    def joinable(self):
        """
        Returns whether this course can currently be joined.
        """
        return not self.saturated and self.active

    @property
    def saturation_level(self):
        """
        Returns the ratio of currently enrolled participants to maximum allowed
        participants.
        """
        return self.participants.count(), self.max_participants

    def get_description_as_html(self):
        return clean_for_description(markdown(self.description))

    # deprecated
    def is_teacher(self, student):
        student = get_user_information(student)
        return self.teacher.filter(id=student.id).exists()

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
        if student:
            student = get_user_information(student)
            context['is_subbed'] = student.course_set.filter(id=self.id).exists()

        if student.user.has_perm('course.change_course', self):
            context['is_teacher'] = True
            context['students'] = self.participants.all()

        return context

    def can_be_archived(self):
        return self.archiving == 't'

    def is_archived(self):
        return self.archiving == 'a'

    def has_description(self):
        return self.description != ''


class Notification(models.Model):
    subject = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ManyToManyField(UserInformation)
