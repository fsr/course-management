from django.shortcuts import render
from course_management.models import course, subject
import collections


def get_all_courses():
    return course.Course.objects.filter(active=True)

def get_all_subjects():
    return subject.Subject.objects.all()

def render_with_default(request, template, context):
    default_context = {
         'active_courses': get_all_courses(),
         'active_subjects': get_all_subjects()
    }
    return render(request, template, collections.ChainMap(context, default_context))
