from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from course_management.models.course import Course
from course_management import forms
from course_management.models.schedule import Schedule, WeeklySlot, DateSlot
from course_management.views.base import render_with_default


@login_required
def add_slot(request: HttpRequest, course_id) -> HttpResponse:

    course = Course.objects.get(id=course_id)

    if course.is_teacher(request.user):

        schedule = course.schedule

        if schedule.is_weekly():
            return _add_weekly_slot(request, course_id, schedule)
        else:
            return _add_date_slot(request, course_id, schedule)

    else:
        raise PermissionDenied()


def _add_weekly_slot(request: HttpRequest, course_id: int, schedule: Schedule):

    if request.method == 'POST':
        data = forms.AddWeeklySlotForm(request.POST)

        if data.is_valid():
            cleaned = data.cleaned_data

            slot = WeeklySlot(
                weekday=cleaned['weekday'],
                timeslot=cleaned['timeslot'],
                location=cleaned['location'],
                schedule=schedule
            )
            slot.save()

            return redirect('course-add-slot', course_id)

    else:
        data = forms.AddWeeklySlotForm()

    return render_with_default(
        request,
        'course/time.html',
        {
            'form': data,
            'schedule': schedule,
            'course_id': course_id,
            'target': 'edit',
        }
    )


def _add_date_slot(request:HttpRequest, course_id, schedule: Schedule):

    if request.method == 'POST':
        data = forms.AddDateForm(request.POST)

        if data.is_valid():
            cleaned = data.cleaned_data

            slot = DateSlot(
                date=cleaned['date'],
                location=cleaned['location'],
                schedule=schedule
            )
            slot.save()

            return redirect('course-add-slot', course_id)
    else:
        data = forms.AddDateForm()

    return render_with_default(
        request,
        'course/time.html',
        {
            'form': data,
            'schedule': schedule,
            'course_id': course_id,
            'target': 'edit'
        }
    )


@login_required()
@require_POST
def remove_slot(request, course_id, slot_id):

    target = request.GET.get('target', None)

    course = Course.objects.get(id=course_id)

    if course.is_teacher(request.user):

        course.schedule.slots.get(id=slot_id).delete()

        return redirect('course-add-slot' if target == 'edit' else 'course', course_id)

    else:
        raise PermissionDenied()

