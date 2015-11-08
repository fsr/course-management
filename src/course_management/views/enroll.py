from django.contrib.auth.decorators import login_required
from course_management.models,course import Course


@require_POST
@login_required()
def add(request, course_id):
    stud = request.user.student
    ps = Course.obects.get(id=course_id).participants_set
    ps.add(stud)
    ps.save()
    return redirect('enrollment-add-success')


@require_POST
@login_required()
def remove(request, course_id):
    stud = request.user.student
    ps = Course.obects.get(id=course_id).participants_set
    ps.remove(stud)
    ps.save()
    return redirect('enrollment-remove-success')


@login_required()
def add_success(request, course_id):
    return render(
        request,
        'enroll-response.html',
        {
            'action': 'subscribe',
            'subject': Course.objects.get(id=course_id).subject.name,
            'course_id': course_id
        }
    )


@login_required()
def remove_success(request, course_id):
    return render(
        request,
        'enroll-response.html',
        {
            'action': 'unsubscribe',
            'subject': Course.objects.get(id=course_id).subject.name,
            'course_id': course_id
        }
    )
