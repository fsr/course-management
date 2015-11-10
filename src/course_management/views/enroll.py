from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from course_management.models.course import Course
from django.shortcuts import redirect
from course_management.views.base import render_with_default
from .course import _course_context



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
    return redirect('register-course-done', course_id)


@require_POST
@login_required()
def remove(request, course_id):
    stud = request.user.student
    course = Course.objects.get(id=course_id)
    ps = course.participants
    ps.remove(stud)
    return redirect('unregister-course-done', course_id)


@login_required()
def enroll_response(request, course_id, action=None):
    session = request.session
    course = Course.objects.get(id=course_id)
    context = _course_context(request, course)
    context['action'] = action
    context['subject'] = course.subject.name
    context['course_id'] = course_id

    if 'enroll-error' in session:
        context['error'] = session['enroll-error']
        del session['enroll-error']
    return render_with_default(request, 'enroll/response.html', context)
