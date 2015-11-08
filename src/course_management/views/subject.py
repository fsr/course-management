from course_management.views.base import render_with_default
from django.core.urlresolvers import reverse

from course_management.models import course, subject


def render_course_overview(request, subjectname):
    active_subject = subject.Subject.objects.filter(name=subjectname).get()
    return render_with_default(request, 'subject.html', {'title': '{name} | iFSR Course Management'.format(name=subjectname),
                                                         'subject': active_subject,
                                                         'backurl': reverse('index'),
                                                         })