from django.db import models


class Schedule(models.Model):

    class Meta:
        abstract = True

class Weekly(Schedule):
    @property
    def slots(self):
        return WeeklySlots.objects.get(schedule=self)

class OneTime(Schedule):

    @property
    def slots(self):
        return DateSlots.objects.get(schedule=self)

class WeeklySlot(models.Model):
    schedule = models.ForeighnKey(Weekly)

class DateSlot(models.Model):
    schedule = models.ForeighnKey(OneTime)
