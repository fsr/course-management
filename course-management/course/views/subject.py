from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _

from course.models import subject
from course.forms import SubjectForm

from util.error.reporting import db_error


def course_overview(request, subjectname):
    user = request.user

    try:
        active_subject = subject.Subject.objects.get(name=subjectname)
    except subject.Subject.DoesNotExist:
        return db_error(request, _('Requested subject does not exist.'))

    if user.is_authenticated:
        cl = list(filter(
            lambda c: c.visible or c.can_modify(user.userinformation),
            active_subject.course_set.filter(archiving='t')
        ))
        for course in cl:
            course.position_in_queue = course.position_in_queue(user)
    else:
        cl = list(active_subject.course_set.filter(visible=True, archiving='t'))



    return render(
        request,
        'subject/info.html',
        {
            'title': subjectname,
            'subject': active_subject,
            'course_list': cl,
            'target': reverse('subject', args=(subjectname,))
        }
    )


def subject_overview(request):
    return render(
        request,
        'subject/overview.html',
        {
            'title': _('Subject Overview'),
            'visible_subjects': subject.Subject.get_visible(),
            'invisible_subjects': subject.Subject.get_invisible()
        }
    )


@login_required()
@permission_required('subject.add_subject')
def create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():

            created = form.save()
            return redirect('subject', created.name)

    else:
        form = SubjectForm()
        form.initial['description'] = _((
            'English is a weakly typed, interpreted language and runs on a '
            'large number of modern humanoids with varying support for '
            'advanced syntax features. Website: https://oed.com'
        ))

    return render(
        request,
        'subject/edit.html',
        {
            'title': _('New Subject'),
            'create': True,
            'form': form
        }
    )


@login_required()
@permission_required('subject.change_subject')
def edit(request, subjectname):
    try:
        subj = subject.Subject.objects.get(name=subjectname)
    except subject.Subject.DoesNotExist:
        return db_error(request, _('Requested subject does not exist.'))

    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subj)

        if 'cancel' not in request.POST and form.is_valid():
            subj.save()

        return redirect('subject', subj.name)

    else:
        form = SubjectForm(instance=subj)

    return render(
        request,
        'subject/edit.html',
        {
            'title': subj.name,
            'create': False,
            'form': form,
            'subject': subj
        }
    )


@login_required()
@require_POST
@permission_required('subject.delete_subject')
def delete(request, subjectname):
    try:
        subj = subject.Subject.objects.get(name=subjectname)
    except subject.Subject.DoesNotExist:
        return db_error(request, _('Requested subject does not exist.'))

    subj.delete()

    return redirect('subject-overview')
