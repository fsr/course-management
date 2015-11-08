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
    schedule = models.ForeignKey(Schedule)


class DateSlot(models.Model):
    schedule = models.ForeignKey(Schedule)
