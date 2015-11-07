from django.shortcuts import render
from course_management.models import course
import collections


def get_all_courses():
    return course.Course.objects.filter(active=True)


def render_with_default(request, template, context):
    default_context = {
         'active_courses': get_all_courses()
    }
    return render(request, template, collections.ChainMap(context, default_context))
