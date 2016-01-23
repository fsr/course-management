from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext as _

from course.models import subject
from course.forms import SubjectForm

from util.error.reporting import db_error


def course_overview(request, subjectname):
    user = request.user

    try:
        active_subject = subject.Subject.objects.get(name=subjectname)
    except subject.Subject.DoesNotExist:
        return db_error(_('Requested subject does not exist.'))

    if user.is_authenticated():
        student = user.userinformation
        cl = filter(
            lambda c: c.active or c.is_teacher(user.userinformation),
            active_subject.course_set.all()
        )
    else:
        cl = active_subject.course_set.filter(active=True)

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


@login_required()
# TODO add permission for viewing this overview, maybe?
def subject_overview(request):
    return render(
        request,
        'subject/overview.html',
        {
            'title': _('Subject Overview'),
            'subjects': subject.Subject.objects.all()
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
        'subject/create.html',
        {
            'title': _('New Subject'),
            'form': form
        }
    )


@login_required()
@permission_required('subject.change_subject')
def edit(request, subjectname):
    try:
        subj = subject.Subject.objects.get(name=subjectname)
    except subject.Subject.DoesNotExist:
        return db_error(_('Requested subject does not exist.'))

    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subj)

        if form.is_valid():

            subj.save()

            return redirect('subject', subj.name)

    else:
        form = SubjectForm(instance=subj)

    return render(
        request,
        'subject/edit.html',
        {
            'title': subj.name,
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
        return db_error(_('Requested subject does not exist.'))

    subj.delete()

    return redirect('subject-overview')
