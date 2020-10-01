from django.contrib import admin

from .models import course, schedule, subject, news
from user.models import UserInformation, Activation

admin.site.register(course.Course)
admin.site.register(course.Notification)
admin.site.register(course.Participation)
admin.site.register(schedule.Schedule)
admin.site.register(schedule.WeeklySlot)
admin.site.register(schedule.DateSlot)
admin.site.register(UserInformation)
admin.site.register(Activation)
admin.site.register(subject.Subject)
admin.site.register(news.News)
