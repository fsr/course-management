from course_management.views.base import render_with_default
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from course_management.forms import EditCourseForm
from django.shortcuts import redirect

from course_management.models import course


def render_course(request, course_id):
    active_course = course.Course.objects.get(id=course_id)
    print(type(course_id))
    return render_with_default(
        request,
        'course/info.html',
        {
            'title': active_course.subject.name,
            'course_id': course_id,
            'is_subbed': active_course.participants.filter(id=request.user.student.id).exists(),
            'backurl': reverse('subject', args=[course_id]),
        }
    )

@login_required()
def edit_course(request, course_id):
    if request.method == "POST":
        form = EditCourseForm(request.POST)
        if form.is_valid():
            c = course.Course.objects.get(id=course_id)
            cleaned = form.cleaned_data
            for prop in (
                'active',
                'description',
                'max_participants'
            ):
                if prop in cleaned:
                    c.__setattr__(prop,cleaned[prop])
            c.save()
            return redirect('course', course_id)
        else:
            return render_with_default(
                request,
                'course/edit.html',
                {
                    'form': form,
                    'course_id': course_id
                }
            )
    else:
        c = course.Course.objects.get(id=course_id)
        form = EditCourseForm(dict(
                active = c.active,
                description = c.description,
                max_participants = c.max_participants
            ))

    return render_with_default(
        request,
        'course/edit.html',
        {
            'form': form,
            'course_id': course_id
        }
    )
