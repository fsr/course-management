from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect

from course.views.base import render_with_default

from course.models import subject
from course.forms import CreateSubjectForm
from util.error.reporting import db_error


def course_overview(request, subjectname):
    user = request.user

    try:
        active_subject = subject.Subject.objects.get(name=subjectname)
    except subject.Subject.DoesNotExist:
        return db_error('Requested subject does not exist.')

    if user.is_authenticated():
        student = user.student
        cl = filter(
            lambda c: c.active or c.is_teacher(student),
            active_subject.course_set.all()
        )
    else:
        cl = active_subject.course_set.filter(active=True)

    return render_with_default(
        request,
        'subject/info.html',
        {
            'title': '{name} | iFSR Course Management'.format(name=subjectname),
            'subject': active_subject,
            'course_list': cl,
            'target': reverse('subject', args=(subjectname,))
        }
    )


@login_required()
# TODO add permission for viewing this overview, maybe?
def subject_overview(request):
    return render_with_default(
        request,
        'subject/overview.html',
        {'subjects': subject.Subject.objects.all() }
    )


@login_required()
@permission_required('subject.add_subject')
def create(request):
    if request.method == 'POST':
        form = CreateSubjectForm(request.POST)
        if form.is_valid():

            data = form.cleaned_data

            created = subject.Subject.objects.create(
                name=data['name'],
                description=data['description']
            )
            return redirect('subject', created.name)

    else:
        form = CreateSubjectForm()

    return render_with_default(
        request,
        'subject/create.html',
        {'form': form}
    )
