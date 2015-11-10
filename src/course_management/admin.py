from django.contrib import admin

from .models import course, schedule, subject
from user_management.models import Student, Activation, Faculty

admin.site.register(course.Course)
admin.site.register(Faculty)
admin.site.register(schedule.Schedule)
admin.site.register(schedule.WeeklySlot)
admin.site.register(schedule.DateSlot)
admin.site.register(Student)
admin.site.register(subject.Subject)
admin.site.register(Activation)
