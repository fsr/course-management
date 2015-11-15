from django.core.urlresolvers import reverse

from course.views.base import render_with_default

from course.models import subject
from util.error.reporting import db_error


def course_overview(request, subjectname):
    user = request.user

    try:
        active_subject = subject.Subject.objects.get(name=subjectname)
    except subject.Subject.DoesNotExist:
        return db_error('Requested subject does not exist.')

    if user.is_authenticated():
        student = user.student
        cl = filter(
            lambda c: c.active or c.is_teacher(student),
            active_subject.course_set.all()
        )
    else:
        cl = active_subject.course_set.filter(active=True)

    return render_with_default(
        request,
        'subject.html',
        {
            'title': '{name} | iFSR Course Management'.format(name=subjectname),
            'subject': active_subject,
            'course_list': cl,
            'target': reverse('subject', args=(subjectname,))
        }
    )
