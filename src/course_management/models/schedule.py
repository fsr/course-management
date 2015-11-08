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
        #return "{type} - {slots}".format(type=self.get__type_display(), slots="; ".join(map(str,self.slots)))
        course = self.course
        return "{} - {} - {}".format(self._type, course.id, course.subject.name)


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
        return "{weekday}, {timeslot}".format(weekday=self.get_weekday_display(), timeslot=self.get_timeslot_display())




class DateSlot(models.Model):
    date = models.DateTimeField()
    place = models.CharField(max_length=100, blank=True)
    schedule = models.ForeignKey(Schedule)

    def __str__(self):
        return "{date}".format(date=self.date)