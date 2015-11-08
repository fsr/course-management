from django.db import models


class Schedule(models.Model):
    TYPES = [
        ('W', "weekly"),
        ('O', 'one time')
    ]

    _type = models.CharField(max_length=1, choices=TYPES)

    @property
    def slots(self):
        if self._type == 'W':
            return WeeklySlot.objects.get(schedule=self)
        else:
            return DateSlot.objects.get(schedule=self)

    def __str__(self):
        return self._type


class WeeklySlot(models.Model):
    WEEKDAYS = [
        ("MON", "Mondays"),
        ("TUE", "Tuesdays"),
        ("WED", "Wednesdays"),
        ("THU", "Thursdays"),
        ("FRI", "Fridays"),
        ("SAT", "Saturdays"),
        ("SUN", "Sundays"),
    ]
    TIMESLOTS = [
        ("I", "1st"),
        ("II", "2nd"),
        ("III", "3rd"),
        ("IV", "4th"),
        ("V", "5th"),
        ("VI", "6th"),
        ("VII", "7th"),
    ]
    weekday = models.CharField(max_length=3, choices=WEEKDAYS)
    timeslot = models.CharField(max_length=3, choices=TIMESLOTS)
    place = models.CharField(max_length=100)
    schedule = models.ForeignKey(Schedule)


class DateSlot(models.Model):
    schedule = models.ForeignKey(Schedule)
