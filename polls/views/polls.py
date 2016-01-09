from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

from polls.forms import PollInterface, QuestionForm, PollForm
from polls.models import Choice, Question, Poll, QLink
from util.error.reporting import db_error


# REVIEW do we need permissions here?
@login_required
def overview(request):
    """
    Controller for the overview page for all poll.
    """
    return render(
            request,
            'polls/overview.html',
            {'polls': Poll.objects.all()}
    )


# TODO add permissions
@login_required
def vote(request, poll_name):
    """
    Form for voting on a poll and handling the submitted results.
    """
    poll = Poll.objects.get(url=poll_name)
    if request.method == 'POST':
        vote_interface = PollInterface(poll, request.POST)

        if vote_interface.is_valid():
            vote_interface.save()
            return redirect('poll-view', poll.url)
    else:
        vote_interface = PollInterface(poll)

    return render(
            request,
            'polls/poll/vote.html',
            {'vote_interface': vote_interface}
    )


# TODO add permissions
@login_required
def results(request, poll_name):
    """
    View the (currents) results for a poll. (Anonymized)
    """
    vote_interface = PollInterface(Poll.objects.get(url=poll_name))

    return render(
            request,
            'polls/poll/results.html',
            {'vote_interface': vote_interface}
    )


# TODO add permissions
@login_required
def view(request, poll_name):
    """
    Look at the poll. Only look, no touch!!!
    """
    return render(
            request,
            'polls/poll/view.html',
            {'poll': Poll.objects.get(url=poll_name)}
    )


# TODO require permissions
@login_required
def edit_questions(request, poll_name):
    """
    Editing form and handler for adding new questions.
    """
    poll = Poll.objects.get(url=poll_name)
    ChoiceForms = inlineformset_factory(Question, Choice, fields=('value',))

    if request.method == 'POST':
        form = QuestionForm(request.POST)

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
        form = QuestionForm()
        cf = ChoiceForms()
    return render(
        request,
        'polls/questions.html',
        {
            'poll': poll,
            'questions': poll.questions_in_order().all(),
            'form': form,
            'choice_forms': cf,
            'old_questions': Question.objects.all()
        }
    )

# TODO require appropriate permissions
@login_required
def remove_question(request, poll_name, qlink_id, question_id):
    """
    Remove the link between a question and a poll (also discards its results).
    """
    poll = Poll.objects.get(url=poll_name)
    qlink = QLink.objects.get(id=qlink_id)

    if qlink.poll == poll and qlink.question.id == int(question_id):
        qlink.delete()
        return redirect('poll-edit-questions', poll.url)
    else:
        return db_error('Inconsistent query. Id\'s do not match.')


# TODO require appropriate permissions
@login_required
def bump_question(request, poll_name, qlink_id, question_id, up=False):
    """
    Move a question up or down in the poll.
    """
    poll = Poll.objects.get(url=poll_name)
    qlink = QLink.objects.get(id=qlink_id)
    if qlink.poll == poll and qlink.question.id == int(question_id):
        try:
            old_obj = qlink.next_higher_to() if up else qlink.next_lower_to()
            pos = qlink.position
            qlink.position = old_obj.position
            old_obj.position = pos
            qlink.save()
            old_obj.save()
        except QLink.DoesNotExist:
            pass
        return redirect('poll-edit-questions', poll.url)
    else:
        return db_error('Inconsistent query.')

# TODO require permissions
@login_required
def add_question(request, poll_name, question_id):
    """
    Create a link between a question and a poll.
    """
    QLink.objects.create(
            poll=Poll.objects.get(url=poll_name),
            question=Question.objects.get(id=question_id)
    )
    return redirect(
            request.GET['target']
            if 'target' in request.GET
            else reverse('poll-view', args=(poll_name,))
    )


# TODO require permission
@login_required
def create(request):
    """
    Create a new, empty poll.
    """
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        if poll_form.is_valid():

            np = poll_form.save(commit=False)

            p = np  # höhö

            if not np.url:
                np.url = p.url_from_name(np.name)

            np.save()

            return redirect('poll-edit-questions', np.url)

    else:
        poll_form = PollForm()

    return render(
        request,
        'polls/poll/create.html',
            {'poll_form': poll_form}
    )
