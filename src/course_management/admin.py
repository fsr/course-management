from django.contrib import admin

from .models import course, faculty, schedule, student, subject, activation

admin.site.register(course.Course)
admin.site.register(faculty.Faculty)
admin.site.register(schedule.Schedule)
admin.site.register(student.Student)
admin.site.register(subject.Subject)
admin.site.register(activation.Activation)
