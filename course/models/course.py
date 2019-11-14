from markdown import markdown
import logging

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import django.utils.timezone

from guardian.models import UserObjectPermission

from . import subject

from user.models import UserInformation, get_user_information

from util.html_clean import clean_for_description


ARCHIVE_STATUSES = (
    ('t', 'auto'),
    ('n', 'never'),
    ('a', 'archived'),
)

class Course(models.Model):
    teacher = models.ManyToManyField(UserInformation, related_name="teacher", blank=True)
    participants = models.ManyToManyField(UserInformation, blank=True, through='Participation')
    active = models.BooleanField(default=False)
    visible = models.BooleanField(default=False)
    subject = models.ForeignKey(subject.Subject, on_delete=models.CASCADE)
    max_participants = models.IntegerField()
    description = models.TextField(blank=True, default="")
    archiving = models.CharField(max_length=1, choices=ARCHIVE_STATUSES)
    start_time = models.DateField(default=django.utils.timezone.now)
    end_time = models.DateField(default=django.utils.timezone.now)

    class IsFull(Exception):
        pass

    class IsInactive(Exception):
        pass

    class IsInvisible(Exception):
        pass

    class IsNotEnrolled(Exception):
        pass

    class IsEnrolled(Exception):
        pass

    class IsArchived(Exception):
        pass


    def __str__(self):
        return self.subject.name

    def enroll(self, student):
        student = get_user_information(student)
        if self._is_participant(student):
            raise self.IsEnrolled
        elif not self.active:
            raise self.IsInactive
        elif self.is_archived():
            raise self.IsArchived
        else:
            if (self.participants.count()):
                ticket_number = Participation.objects.filter(course=self).reverse()[0].ticket_number + 1
            else:
                ticket_number = 1
            Participation.objects.create(participant=student, course=self, ticket_number=ticket_number)

    def unenroll(self, student):

        student = get_user_information(student)

        if self._is_participant(student):
            self.participants.remove(student)
        else:
            raise self.IsNotEnrolled
        # TODO: send notification to first in waiting list

    def _is_participant(self, student):
        student = get_user_information(student)
        return student in self.participants.all()

    def is_participant(self, student):
        return self._is_participant(get_user_information(student)) and not self.is_archived()

    @property
    def saturated(self):
        (curr, max) = self.saturation_level
        return curr >= max

    @property
    def joinable(self):
        """
        Returns whether this course can currently be joined.
        """
        return not self.saturated and self.is_active() and self.is_visible()

    @property
    def saturation_level(self):
        """
        Returns the ratio of currently enrolled participants to maximum allowed
        participants.
        """
        return self.participants.count(), self.max_participants

    @property
    def enrolled_students(self):
        return min(self.participants.count(), self.max_participants)

    @property
    def students_on_queue(self):
        return max(self.participants.count() - self.max_participants, 0)

    def get_description_as_html(self):
        return clean_for_description(markdown(self.description))

    def get_distinct_locations(self):
        return self.schedule.slots.values_list('location', flat=True).distinct()

    def get_queue(self):
        return Participation.objects.filter(course=self)[self.max_participants:]

    def position_in_queue(self, student):
        queue = list(self.get_queue())
        if len(queue) == 0:
            return 0
        users = [p.participant for p in queue]
        user = get_user_information(student)
        if not user in users:
            return 0
        return users.index(user) + 1

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
            'course_is_visible': self.visible,
        }
        if student:
            student = get_user_information(student)
            context['position_in_queue'] = self.position_in_queue(student)
            context['is_subbed'] = student.course_set.filter(id=self.id).exists()

            if self.is_teacher(student):
                context['is_teacher'] = True
                context['students'] = self.participants.all()

        return context

    def can_be_archived(self):
        return self.archiving == 't'

    def is_archived(self):
        return self.archiving == 'a'

    def has_description(self):
        return self.description != ''

    def is_teacher(self, student):
        return student.user.has_perm('change_course', self) \
                and student.user.has_perm('delete_course', self)

    def is_active(self):
        return self.active and not self.is_archived()

    def is_visible(self):
        return self.visible and not self.is_archived()


class Notification(models.Model):
    subject = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ManyToManyField(UserInformation)

class Participation(models.Model):
    participant = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    ticket_number = models.IntegerField()

    class Meta:
        ordering = ['ticket_number']

