from django.core.urlresolvers import reverse

from course_management.views.base import render_with_default

from course_management.models import subject
from util.error.reporting import db_error


def course_overview(request, subjectname):
    try:
        active_subject = subject.Subject.objects.get(name=subjectname)
    except subject.Subject.DoesNotExist:
        return db_error('Requested subject does not exist.')
    return render_with_default(
        request,
        'subject.html',
        {
            'title': '{name} | iFSR Course Management'.format(name=subjectname),
            'subject': active_subject,
            'course_list': active_subject.course_set.all,
            'target': reverse('subject', args=(subjectname,))
        }
    )
