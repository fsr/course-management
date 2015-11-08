from course_management.views.base import render_with_default
from django.core.urlresolvers import reverse

from course_management.models import course


def render_course(request, courseid):
    active_course = course.Course.objects.get(id=courseid)
    return render_with_default(request, 'course.html', {'title': 'Course',
                                                        'course': active_course,
                                                        'backurl': reverse('subject', args=[active_course.subject.name]),
                                                        })