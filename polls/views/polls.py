from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

from util.error.reporting import db_error

from polls import forms
from polls.forms import VoteInterface
from polls.models import Choice, Question, Poll, QLink


# REVIEW do we need permissions here?
@login_required
def overview(request):
    return render(
            request,
            'polls/overview.html',
            {'polls': Poll.objects.all()}
    )


# TODO add permissions
@login_required
def vote(request, poll_name):
    poll = Poll.objects.get(url=poll_name)
    if request.method == 'POST':
        vi = VoteInterface(poll, request.POST)

        if vi.is_valid():
            vi.save()
            return redirect(
                    'poll-view',
                    poll.url
            )
    else:
        vi = VoteInterface(poll)

    return render(
            request,
            'polls/poll/vote.html',
            {'vi': vi}
    )


# TODO add permissions
@login_required
def results(request, poll_name):
    vi = VoteInterface(Poll.objects.get(url=poll_name))

    return render(
            request,
            'polls/poll/results.html',
            {'vi': vi}
    )


# TODO add permissions
@login_required
def view(request, poll_name):
    return render(
            request,
            'polls/poll/view.html',
            {'poll': Poll.objects.get(url=poll_name)}
    )


# TODO require permissions
@login_required
def edit_questions(request, poll_name):
    poll = Poll.objects.get(url=poll_name)
    ChoiceForms = inlineformset_factory(Question, Choice, fields=('value',))

    if request.method == 'POST':
        form = forms.QuestionForm(request.POST)

        if form.is_valid():
            q = form.save(commit=False)

            cf = ChoiceForms(request.POST, instance=q)

            if cf.is_valid():

                q.save()
                cf.save()

                QLink.objects.create(
                        poll=poll,
                        question=q
                )

                return redirect('poll-edit-questions', poll.url)
        else:
            cf = ChoiceForms()
    else:
        form = forms.QuestionForm()
        cf = ChoiceForms()
    return render(
        request,
        'polls/questions.html',
        {
            'poll': poll,
            'questions': sorted(poll.questions.all(), lambda a: a.position),
            'form': form,
            'choice_forms': cf,
            'old_questions': Question.objects.all()
        }
    )

# TODO require appropriate permissions
@login_required
def remove_question(request, poll_name, qlink_id, question_id):
    poll = Poll.objects.get(url=poll_name)
    qlink = QLink.objects.get(id=qlink_id)

    if qlink.poll == poll and qlink.question.id == int(question_id):
        qlink.delete()
        return redirect('poll-edit-questions', poll.url)
    else:
        return db_error('Inconsistent query.')


# TODO require appropriate permissions
@login_required
def bump_question(request, poll_name, qlink_id, question_id, up=False):
    poll = Poll.objects.get(url=poll_name)
    qlink = QLink.objects.get(id=qlink_id)
    if qlink.poll == poll and qlink.question.id == int(question_id):
        new_pos = qlink.position + (1 if up else (-1))
        try:
            old_obj = Qlink.objects.get(poll=poll, question=qlink.question, position=qlink.position)
            old_obj.position = qlink.position
            old_obj.save()
        except Qlink.DoesNotExist:
            pass
        qlink.position = new_pos
        qlink.save()
        return redirect('poll-edit-questions', poll.url)
    else:
        return db_error('Inconsistent query.')

# TODO require permissions
@login_required
def add_question(request, poll_name, question_id):
    target = request.GET['target'] if 'target' in request.GET else reverse('poll-view', args=(poll_name,))
    QLink.objects.create(
            poll=Poll.objects.get(url=poll_name),
            question=Question.objects.get(id=question_id)
    )
    return redirect(
            target
    )


# TODO require permission
@login_required
def create(request):
    if request.method == 'POST':
        poll_form = forms.PollForm(request.POST)
        if poll_form.is_valid():

            np = poll_form.save(commit=False)

            p = np  # höhö

            if not np.url:
                np.url = n.url_from_name(np.name)

            np.save()

            return redirect('poll-edit-questions', np.url)

    else:
        poll_form = forms.PollForm()

    return render(
        request,
        'polls/poll/create.html',
            {'poll_form': poll_form}
    )
