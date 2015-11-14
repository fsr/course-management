import functools

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from course_management.models.course import Course
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
            return db_error('This course does not seem to exist, sorry.')
        if curr_course.is_teacher(request.user):
            return func(request, course_id, *args, **kwargs)
        else:
            raise PermissionDenied()
    return wrapped
