from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext as _

from course.models import news
from course.forms import NewsForm

from util.error.reporting import db_error

@login_required()
@permission_required('subject.add_subject')
def create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = NewsForm()
        form.initial['entry'] = _((
            'English is a weakly typed, interpreted language and runs on a '
            'large number of modern humanoids with varying support for '
            'advanced syntax features. Website: https://oed.com'
        ))

    return render(
        request,
        'news/create.html',
        {
            'title': _('New News'),
            'form': form
        }
    )


@login_required()
@permission_required('subject.change_subject')
def edit(request, headline):
    try:
        subj = subject.Subject.objects.get(name=headline)
    except subject.Subject.DoesNotExist:
        return db_error(_('Requested News does not exist.'))

    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subj)

        if 'cancel' not in request.POST and form.is_valid():
            subj.save()

        return redirect('subject', subj.name)

    else:
        form = SubjectForm(instance=subj)

    return render(
        request,
        'news/edit.html',
        {
            'title': subj.name,
            'form': form,
            'subject': subj
        }
    )
