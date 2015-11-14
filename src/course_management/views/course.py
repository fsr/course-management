import functools

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied

from course_management.models.schedule import Schedule
from course_management.models.subject import Subject
from course_management.views.base import render_with_default
from course_management.models.course import Course
from course_management.forms import EditCourseForm, CreateCourseForm, AddTeacherForm
from user_management.models import Student
from util import html_clean


def course(request, course_id):
    return render_with_default(
        request,
        'course/info.html',
        _course_context(request, course_id)
    )


def _course_context(request, course_id):

    if isinstance(course_id, Course):
        active_course = course_id
        course_id = course_id.id
    else:
        active_course = Course.objects.get(id=course_id)

    participants_count, max_participants = active_course.saturation_level
    sub_name = active_course.subject.name
    context = {
        'title': sub_name,
        'course_id': course_id,
        'course': active_course,
        'backurl': reverse('subject', args=[sub_name]),
        'participants_count': participants_count,
        'max_participants': max_participants,
        'course_is_active': active_course.active,
    }
    user = request.user

    if user.is_authenticated():

        context['is_subbed'] = user.student.course_set.filter(id=course_id).exists()

        if active_course.is_teacher(user):
            context['is_teacher'] = True
            context['students'] = active_course.participants.all()

    return context


@login_required()
def edit_course(request, course_id):

    if request.method == "POST":

        form = EditCourseForm(request.POST)

        if form.is_valid():

            c = Course.objects.get(id=course_id)
            cleaned = form.cleaned_data

            for prop in filter(cleaned.__contains__,(
                'active',
                'max_participants'
            )):

                c.__setattr__(prop,cleaned[prop])

            if 'description' in cleaned:
                c.description = cleaned['description']

            c.save()
            return redirect('course', course_id)

    else:
        c = Course.objects.get(id=course_id)
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
            'course_id': course_id,
            'allowed_tags': html_clean.DESCR_ALLOWED_TAGS,
            'course_is_active': c.active,
        }
    )


def must_be_teacher(func):
    @functools.wraps(func)
    @login_required()
    def wrapped(request, course_id, *args, **kwargs):
        curr_course = Course.objects.get(id=course_id)
        if curr_course.is_teacher(request.user):
            return func(request, course_id, *args, **kwargs)
        else:
            raise PermissionDenied()
    return wrapped


@must_be_teacher
@require_POST
def activate(request, course_id):
    curr_course = Course.objects.get(id=course_id)
    curr_course.active = True
    curr_course.save()
    return redirect('course', course_id)


@must_be_teacher
@require_POST
def deactivate(request, course_id):
    curr_course = Course.objects.get(id=course_id)
    curr_course.active = False
    curr_course.save()
    return redirect('course', course_id)


@permission_required('course.add_course')
def create(request):

    if request.method == 'POST':
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data

            active = cleaned.get('active', False)

            created = Course.objects.create(
                schedule=Schedule.objects.create(_type=cleaned['schedule']),
                active=active if active is not None else False,
                subject=Subject.objects.get(id=int(cleaned['subject'])),
                max_participants=cleaned['max_participants'],
                description=cleaned['description']
            )

            created.teacher.add(request.user.student)

            return redirect('course', created.id)
    else:
        form = CreateCourseForm()

    return render_with_default(request, 'course/create.html', {'form': form})


@login_required()
@must_be_teacher
def add_teacher(request, course_id):
    context = {'course_id': course_id, 'target': reverse('add-teacher', args=(course_id,))}
    curr_course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data['username'])

                curr_course.teacher.add(user.student)

                return redirect('add-teacher', course_id)
            except User.DoesNotExist:
                context['error'] = 'The username you entered does not exist in my database, sorry :('
    else:
        form = AddTeacherForm()

    context['form'] = form
    context['teachers'] = curr_course.teacher

    return render_with_default(
        request,
        'course/teacher.html',
        context
    )


@login_required()
@must_be_teacher
@require_POST
def remove_teacher(request, course_id, teacher_id):
    t = request.GET.get('target', None)
    Course.objects.get(id=course_id).teacher.remove(Student.objects.get(id=teacher_id))
    target = reverse('course', args=(course_id,)) if t is None else t
    return redirect(target)
