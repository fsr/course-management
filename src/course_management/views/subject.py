from django.core.urlresolvers import reverse

from course_management.views.base import render_with_default

from course_management.models import subject


def course_overview(request, subjectname):
    active_subject = subject.Subject.objects.get(name=subjectname)
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
