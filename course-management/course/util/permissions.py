import functools

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _
from django.urls import reverse
from django.shortcuts import redirect

from course.models.course import Course
from util.error.reporting import db_error


def needs_teacher_permissions(func):
    """
    The decorated function must take at least 2 parameters, the request, and a Course object or an id for a course.

    If the current user is registered as a teacher for the course the decorated function is executed, else
    the user is redirected to the login page

    :param func:
    :return:
    """
    @functools.wraps(func)
    @login_required()
    def wrapped(request, course_id, *args, **kwargs):
        try:
            curr_course = Course.objects.get(id=course_id) if not isinstance(course_id, Course) else course_id
        except Course.DoesNotExist:
            return db_error(request, _('This course does not seem to exist, sorry.'))
        if has_teacher_permissions(request.user.userinformation, curr_course):
            return func(request, course_id, *args, **kwargs)
        else:
            return redirect(reverse('login')+'?next='+request.path)
    return wrapped

def has_teacher_permissions(student, course):
    """
    Returns true if the student ist allowed to change and delete the course,
    i.e. they are a teacher or have general permissions to change and edit
    course objects
    """
    return course.can_modify(student) or (
            student.user.has_perm('course.change_course')
            and student.user.has_perm('course.change_course')
    )
