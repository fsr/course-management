import functools

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _

from course.models.course import Course
from util.error.reporting import db_error


def needs_teacher_permissions(func):
    """
    The decorated function must take at least 2 parameters, the request, and a Course object or an id for a course.

    If the current user is registered as a teacher for the course the decorated function is executed, else a
     PermissionError is raised

    :param func:
    :return:
    """
    @functools.wraps(func)
    @login_required()
    def wrapped(request, course_id, *args, **kwargs):
        try:
            curr_course = Course.objects.get(id=course_id) if not isinstance(course_id, Course) else course_id
        except Course.DoesNotExist:
            return db_error(_('This course does not seem to exist, sorry.'))
        if request.user.has_perm('course.change_course', curr_course) or request.user.has_perm('course.change_course'):
            return func(request, course_id, *args, **kwargs)
        else:
            raise PermissionDenied()
    return wrapped