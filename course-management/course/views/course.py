from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from guardian.shortcuts import assign_perm
from guardian.shortcuts import remove_perm

from course.forms import CourseForm, AddTeacherForm, NotifyCourseForm
from course.models.course import Course
from course.models.schedule import Schedule
from course.models.subject import Subject
from course.util.permissions import needs_teacher_permissions
from user.models import UserInformation
from user.forms import ContactForm
from util import html_clean
from util.error.reporting import db_error
from util.routing import redirect_unless_target
import itertools

DEFAULT_COURSE_DESCRIPTION = """\
#### The Hitchhikers Guide To The Galaxy

We will explore the universe.

##### Materials

- a towel
- lots of courage
"""

CONTACT_FOOTER = """
-------------------
This message has been sent via the Course Mangement System at https://kurse.ifsr.de.
Sent by: """

BLANK_FOOTER = """
-------------------
This message has been sent via the Course Mangement System at https://kurse.ifsr.de.
"""



def course(request: HttpRequest, course_id: str):
    """
    Controller for single course info page

    :param request: request object
    :param course_id: id for the course
    :return:
    """
    try:
        current_course = Course.objects.get(id=course_id)

        if hasattr(request.user, 'userinformation'):
            user = request.user.userinformation

            if isinstance(user, UserInformation):
                context = current_course.as_context(user)
            else:
                context = current_course.as_context()
        else:
            context = current_course.as_context()

        session = request.session
        if 'enroll-error' in session:
            context['error'] = session['enroll-error']
            del session['enroll-error']

        return render(
            request,
            'course/info.html',
            context
        )
    except Course.DoesNotExist:
        return db_error(request, _('Requested course does not exist.'))


@needs_teacher_permissions
def participants_list(request, course_id):
    try:
        current_course = Course.objects.get(id=course_id)

        return render(
            request,
            'course/attendees.html',
            {'course': current_course}
        )
    except Course.DoesNotExist:
        return db_error(request, _('Requested course does not exist.'))


@needs_teacher_permissions
def edit_course(request: HttpRequest, course_id: str):
    """
    Edit form for changing a course and handler for submitted data.

    :param request: request object
    :param course_id: id for the course
    :return:
    """
    try:
        current_course = Course.objects.get(id=course_id)
        current_schedule = Schedule.objects.get(course_id=course_id)
    except Course.DoesNotExist:
        return db_error(request, _('Requested course does not exist.'))

    if request.method == "POST":
        form = CourseForm(request.POST, instance=current_course)

        if form.is_valid():
            current_course.save()
            current_schedule.set_type(request.POST['schedule_type'])
            current_schedule.save()
            return redirect('course', course_id)

    else:
        # FIXME(feliix42): Manually setting the start & end date here is required beacuse I just can't get django to format the date correctly in the Form setup
        form = CourseForm(instance=current_course,initial={
            'schedule_type':current_schedule.get_type(),
            'start_time': current_course.start_time.strftime('%Y-%m-%d'),
            'end_time': current_course.end_time.strftime('%Y-%m-%d')
        })
    return render(
        request,
        'course/edit.html',
        {
            'title': _('Edit course'),
            'form': form,
            'create': False,
            'course_id': course_id,
            'allowed_tags': html_clean.DESCR_ALLOWED_TAGS,
            'course_is_active': current_course.active,
        }
    )


@needs_teacher_permissions
@require_POST
def toggle(request: HttpRequest, course_id: str, active: bool):
    """
    Toggle course status (active/inactive)

    :param request: request information
    :param course_id:
    :param active: active/inactive
    :return:
    """
    # TODO: Delete me
    try:
        curr_course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return db_error(request, _('Requested course does not exist.'))

    curr_course.active = active
    if not active:
        curr_course.participants.clear()
        curr_course.queue.clear()
    curr_course.save()
    return redirect('course', course_id)


@permission_required('course.add_course')
def create(request):

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            created = form.save(commit=False)
            created.save()
            created.teacher.add(request.user.userinformation)

            Schedule.objects.create(_type=request.POST['schedule_type'], course=created)

            assign_perm(
                'change_course',
                request.user,
                created
            )
            assign_perm(
                'delete_course',
                request.user,
                created
            )

            return redirect('course', created.id)
    else:
        form = CourseForm(initial={
            'description': DEFAULT_COURSE_DESCRIPTION,
            'max_participants': 30,
            'archiving': 't'
        })
        if 'subject' in request.GET:
            subj = int(request.GET['subject'][0])
            if Subject.objects.filter(id=subj).exists():
                form.initial['subject'] = subj

    return render(
        request,
        'course/edit.html',
        {
            'title': _('New Course'),
            'form': form,
            'create': True
        }
    )


@login_required()
@require_POST
@needs_teacher_permissions
def delete(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return db_error(request, _('Requested course does not exist.'))

    subj = course.subject.name

    course.delete()
    return redirect('subject', subj)


@needs_teacher_permissions
def add_teacher(request, course_id):
    context = {
        'title': _('Edit Teachers'),
        'course_id': course_id,
        'target': reverse('add-teacher', args=(course_id,))
    }

    try:
        curr_course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return db_error(request, _('Requested course does not exist.'))

    if request.method == 'POST':
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data['username'])

                curr_course.teacher.add(user.userinformation)
                assign_perm(
                    'change_course',
                    user,
                    curr_course
                )
                assign_perm(
                    'delete_course',
                    user,
                    curr_course
                )

                return redirect('add-teacher', course_id)
            except User.DoesNotExist:
                context['error'] = _('The username you entered does not exist.')
    else:
        form = AddTeacherForm()

    context['form'] = form
    context['teachers'] = curr_course.teacher

    return render(
        request,
        'course/teachers.html',
        context
    )


@needs_teacher_permissions
@require_POST
def remove_teacher(request, course_id, teacher_id):
    try:
        curr_course = Course.objects.get(id=course_id)
        userinfo = UserInformation.objects.get(id=teacher_id)
        curr_course.teacher.remove(userinfo)
        remove_perm(
            'change_course',
            userinfo.user,
            curr_course
        )
        remove_perm(
            'delete_course',
            userinfo.user,
            curr_course
        )
    except Course.DoesNotExist:
        return db_error(request, _('Requested course does not exist.'))
    except UserInformation.DoesNotExist:
        return db_error(request, _('Requested student does not exist.'))
    return redirect_unless_target(request, 'course', course_id)


@needs_teacher_permissions
def notify(request: HttpRequest, course_id):
    if request.method == 'POST':
        form = NotifyCourseForm(request.POST)
        if form.is_valid():
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return db_error(request, _('Requested course does not exist.'))

            email = request.user.email
            show_sender = form.cleaned_data['show_sender'] and email

            if show_sender:
                content = form.content + CONTACT_FOOTER + email
            else:
                content = form.content + BLANK_FOOTER

            for student in itertools.chain(course.participants.all(), course.teacher.all()):
                student.user.email_user("[iFSR Course Manager] " + form.subject, content)

            return redirect('notify-course-done', course_id)

    else:
        form = NotifyCourseForm()

    return render(
        request,
        'course/notify.html',
        {
            'title': _('Notify Course'),
            'form': form,
            'course_id': course_id
        }
    )


def notify_done(request, course_id):
    return render(
        request,
        'course/notify-done.html',
        {
            'course_id': course_id
        }
    )


@needs_teacher_permissions
def remove_student(request: HttpRequest, course_id:str, student_id:str):
    try:
        course = Course.objects.get(id=course_id)
        course.unenroll(student_id)
    except Course.DoesNotExist:
        return db_error(request, _('Requested course does not exist.'))
    except Course.IsEnrolled:
        return db_error(request, _('Requested student is not enrolled in this course.'))

    return redirect('course', course_id)


@needs_teacher_permissions
def attendee_list(request, course_id):
    if 'slots' in request.GET:
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return db_error(request, _('Requested course does not exist.'))

        # handle empty string (== no number) as input
        try:
            slots = int(request.GET['slots'])
        except ValueError:
            slots = 0

        return render(
                request,
                'course/attendee-list.html',
                {
                    'attendees': course.participants.all(),
                    'slots': range(slots)
                }
        )
    return redirect('course-participants', course_id)

def contact_teachers(request, course_id):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return db_error(request, _('Requested course does not exist.'))

            subject = "[CM contact form] " + form.subject
            content = form.content + CONTACT_FOOTER + request.user.email

            for teacher in course.teacher.all():
                teacher.user.email_user(subject, content)

            return redirect('contact-teachers-done', course_id)

    else:
        form = ContactForm()

    return render(
        request,
        'course/contact-teachers.html',
        {
            'title': _('Notify Course'),
            'form': form,
            'course_id': course_id
        }
    )
