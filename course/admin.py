from django.contrib import admin

from .models import course, schedule, subject
from user.models import UserInformation, Activation, Faculty, StudentInformation

admin.site.register(course.Course)
admin.site.register(Faculty)
admin.site.register(schedule.Schedule)
admin.site.register(schedule.WeeklySlot)
admin.site.register(schedule.DateSlot)
admin.site.register(UserInformation)
admin.site.register(subject.Subject)
admin.site.register(Activation)
admin.site.register(StudentInformation)
