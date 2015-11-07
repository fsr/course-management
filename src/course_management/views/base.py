from django.shortcuts import render
from course_management.models import course, subject
from django.db.models import Count
import collections


def get_relevant_subjects():
    return subject.Subject.objects.annotate(course_count=Count('course')).filter(course_count__gt=0)

def render_with_default(request, template, context):
    default_context = {
         'active_subjects': get_relevant_subjects()
    }
    return render(request, template, collections.ChainMap(context, default_context))
