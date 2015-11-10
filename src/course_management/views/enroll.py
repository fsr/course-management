from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from course_management.models.course import Course
from django.shortcuts import redirect
from course_management.views.base import render_with_default



@require_POST
@login_required()
def add(request, course_id):
    user = request.user
    stud = user.student
    course = Course.objects.get(id=course_id)
    ps = course.participants
    session = request.session

    if ps.filter(id=user.id).exists():
        session['enroll-error'] = 'You are already enrolled in this course.'
    elif ps.count() >= course.max_participants:
        session['enroll-error'] = 'Sorry, this course is full.'
    else:
        if 'enroll-error' in session:
            del session['enroll-error']
        ps.add(stud)
    return redirect('enrollment-add-done', course_id)


@require_POST
@login_required()
def remove(request, course_id):
    stud = request.user.student
    course = Course.objects.get(id=course_id)
    ps = course.participants
    ps.remove(stud)
    return redirect('enrollment-remove-done', course_id)


@login_required()
def add_response(request, course_id):
    session = request.session
    context = {
        'action': 'subscribe',
        'subject': Course.objects.get(id=course_id).subject.name,
        'course_id': course_id
    }
    if 'enroll-error' in session:
        context['error'] = session['enroll-error']
        del session['enroll-error']
    return render_with_default(
        request,
        'enroll/response.html',
        context
    )


@login_required()
def remove_response(request, course_id):
    return render_with_default(
        request,
        'enroll/response.html',
        {
            'action': 'unsubscribe',
            'subject': Course.objects.get(id=course_id).subject.name,
            'course_id': course_id
        }
    )
