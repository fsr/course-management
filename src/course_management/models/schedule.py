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
            return WeeklySlot.objects.filter(schedule=self)
        else:
            return DateSlot.objects.filter(schedule=self)

    def __str__(self):
        slots = ""
        first = True
        if self._type == 'W':
            for slot in self.slots:
                if first:
                    slots += "{weekday} {timeslot}".format(weekday=slot.weekday, timeslot=slot.timeslot)
                    first = False
                else:
                    slots += ", {weekday} {timeslot}".format(weekday=slot.weekday, timeslot=slot.timeslot)
        else:
            for slot in self.slots:
                if first:
                    slots += "{date}".format(date=slot.date)
                else:
                    slots += ", {date}".format(date=slot.date)
        return "{type} - {slots}".format(type=self._type, slots=slots)


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
    place = models.CharField(max_length=100, blank=True)
    schedule = models.ForeignKey(Schedule)

    def __str__(self):
        return "{weekday} {timeslot}".format(weekday=self.weekday, timeslot=self.timeslot)




class DateSlot(models.Model):
    date = models.DateTimeField()
    place = models.CharField(max_length=100, blank=True)
    schedule = models.ForeignKey(Schedule)

    def __str__(self):
        return "{date}".format(date=self.date)