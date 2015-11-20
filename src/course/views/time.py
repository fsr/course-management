from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from course.models.course import Course
from course import forms
from course.models.schedule import Schedule, WeeklySlot, DateSlot
from django.shortcuts import render
from course.util.permissions import needs_teacher_permissions
from util.error.reporting import db_error
from util.routing import redirect_unless_target


@login_required
@needs_teacher_permissions
def edit_slot(request: HttpRequest, course_id):

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return db_error('This course does not exist.')

    schedule = course.schedule

    if schedule.is_weekly():
        form_type = forms.WeeklySlotForm
    else:
        form_type = forms.DateForm

    if request.method == 'POST':
        form = form_type(request.POST)

        if form.is_valid():

            slot = form.save(commit=False)
            slot.schedule = schedule
            slot.save()
            return redirect('course-edit-slot', course_id)

    else:
        form = form_type()

    return render(
        request,
        'course/time.html',
        {
            'title': 'Edit Schedule',
            'form': form,
            'schedule': schedule,
            'course_id': course_id,
            'target': 'course-edit-slot',
        }
    )


@needs_teacher_permissions
@require_POST
def remove_slot(request, course_id, slot_id):

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return db_error(
            'The specified course does not exist. Please try again. '
            'If this error persists, contact an administrator and include the url "{}"'
            ''.format(request.path)
        )

    try:
        course.schedule.slots.get(id=slot_id).delete()
    except (WeeklySlot.DoesNotExist, DateSlot.DoesNotExist):
        return db_error(
            'The slot you\'re trying to remove does not exist. Please try again. '
            'If this error persists, contact an administrator and include the url "{}"'
            ''.format(request.path)
        )

    return redirect_unless_target(request, 'course', course_id)
