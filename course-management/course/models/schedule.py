from django.db import models
from django.utils.translation import gettext_lazy as _

from . import course


WEEKDAYS = [
    ("MON", _("Mondays")),
    ("TUE", _("Tuesdays")),
    ("WED", _("Wednesdays")),
    ("THU", _("Thursdays")),
    ("FRI", _("Fridays")),
    ("SAT", _("Saturdays")),
    ("SUN", _("Sundays")),
]
TIMESLOTS = [
    ("I", _("1st")),
    ("II", _("2nd")),
    ("III", _("3rd")),
    ("IV", _("4th")),
    ("V", _("5th")),
    ("VI", _("6th")),
    ("VII", _("7th")),
]


class Schedule(models.Model):
    TYPES = [
        ('W', _("weekly")),
        ('O', _('one time')),
    ]

    _type = models.CharField(max_length=1, choices=TYPES)
    course = models.OneToOneField(course.Course, on_delete=models.CASCADE)

    def is_weekly(self):
        """
        Returns whether this course operates on a weekly schedule
        """
        return self._type == 'W'

    def is_one_time(self):
        """
        Returns whether this course happens only a distinct number of times.
        """
        return self._type == 'O'

    @property
    def slots(self):
        if self.is_weekly():
            return WeeklySlot.objects.filter(schedule=self)
        else:
            return DateSlot.objects.filter(schedule=self)

    def get_type(self):
        return self._type

    def set_type(self, type):
        self._type = type

    def __str__(self):
        #return "{type} - {slots}".format(type=self.get__type_display(), slots="; ".join(map(str,self.slots)))
        course = self.course
        return "{} - {} - {}".format(self._type, course.id, course.subject.name)


class WeeklySlot(models.Model):
    weekday = models.CharField(max_length=3, choices=WEEKDAYS)
    timeslot = models.CharField(max_length=3, choices=TIMESLOTS)
    location = models.CharField(max_length=100, blank=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return "{weekday}, {timeslot}".format(
            weekday=self.get_weekday_display(),
            timeslot=self.get_timeslot_display()
        )

    def as_summary(self):
        return '{} {} at {}'.format(self.weekday, self.timeslot, self.place)


class DateSlot(models.Model):
    date = models.DateTimeField()
    location = models.CharField(max_length=100, blank=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return self.date.strftime("%d.%m.%Y, %H:%M")

    def as_summary(self):
        return '{} at {}'.format(self.date, self.place)
