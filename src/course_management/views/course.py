from course_management.views.base import render_with_default
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from course_management.forms import EditCourseForm
from django.shortcuts import redirect
import bleach

from course_management.models import course


def render_course(request, course_id):
    active_course = course.Course.objects.get(id=course_id)
    participants_count, max_participants = active_course.saturation_level
    context = {
        'title': active_course.subject.name,
        'course_id': course_id,
        'course': active_course,
        'backurl': reverse('subject', args=[active_course.subject.name]),
        'participants_count': participants_count,
        'max_participants': max_participants,
    }

    if request.user.is_authenticated():
        context['is_subbed'] = active_course.participants.filter(id=request.user.student.id).exists()

        if active_course.teacher.filter(user=request.user).exists():
            context['is_teacher'] = True
            context['students'] = active_course.participants.all()

    return render_with_default(
        request,
        'course/info.html',
        context
    )

@login_required()
def edit_course(request, course_id):
    if request.method == "POST":
        form = EditCourseForm(request.POST)
        if form.is_valid():
            c = course.Course.objects.get(id=course_id)
            cleaned = form.cleaned_data

            for prop in filter(cleaned.__contains__,(
                'active',
                'max_participants'
            )):

                c.__setattr__(prop,cleaned[prop])


            if 'description' in cleaned:
                c.description = bleach.clean(cleaned['description'], strip=True)

            c.save()
            return redirect('course', course_id)

    else:
        c = course.Course.objects.get(id=course_id)
        form = EditCourseForm({
                'active': c.active,
                'description': c.description,
                'max_participants': c.max_participants
            })

    return render_with_default(
        request,
        'course/edit.html',
        {
            'form': form,
            'course_id': course_id
        }
    )
