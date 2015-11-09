from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from course_management.models.course import Course



@require_POST
@login_required()
def add(request, course_id):
    stud = request.user.student
    course = Course.obects.get(id=course_id)
    ps = course.participants_set
    if stud in participants_set:
        request.session['enroll-error'] = 'You are already enrolled in this course.'
    elif len(ps) >= course.max_participants:
        request.session['enroll-error'] = 'Sorry, this course is full.'
    else:
        del request.session['enroll-error']
        ps.add(stud)
        ps.save()
    return redirect('enrollment-add-done')


@require_POST
@login_required()
def remove(request, course_id):
    stud = request.user.student
    course = Course.obects.get(id=course_id)
    ps = course.participants_set
    ps.remove(stud)
    ps.save()
    return redirect('enrollment-remove-done')


@login_required()
def add_response(request, course_id):
    context = {
        'action': 'subscribe',
        'subject': Course.objects.get(id=course_id).subject.name,
        'course_id': course_id
    }
    if 'enroll-error' in user.session:
        context['error'] = user.session['enroll-error']
        del user.session['enroll-error']
    return render(
        request,
        'enroll/response.html',
        context
    )


@login_required()
def remove_response(request, course_id):
    return render(
        request,
        'enroll/response.html',
        {
            'action': 'unsubscribe',
            'subject': Course.objects.get(id=course_id).subject.name,
            'course_id': course_id
        }
    )
