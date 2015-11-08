from django.shortcuts import render
from course_management.models import subject
import collections


def render_with_default(request, template, context):
    default_context = {
         'active_subjects': subject.Subject.get_active()
    }
    return render(request, template, collections.ChainMap(context, default_context))
