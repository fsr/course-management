from course_management.views.base import render_with_default

from course_management.models import course, subject


def render_course_overview(request, subjectname):
    return render_with_default(request, 'subject.html', {'title': '{name} | iFSR Course Management'.format(name=subjectname),
                                                         'courses': get_courses_by_subjectname(subjectname)})


def get_courses_by_subjectname(subjectname):
    opened_subject = subject.Subject.objects.filter(name=subjectname)
    return course.Course.objects.filter(subject=opened_subject)