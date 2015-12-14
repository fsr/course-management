from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from polls.models import Choice, Question, Poll
from polls import forms


def vote(request, poll_name):
    pass


def results(request, poll_name):
    pass


def view(request, poll_name):
    pass


# TODO require permissions
@login_required
def edit_questions(request, poll_name):
    poll = Poll.objects.get(url=poll_name)
    ChoiceForms = inlineformset_factory(Question, Choice, fields=('value',))

    if request.method == 'POST':
        form = forms.QuestionForm(request.POST)

        if form.is_valid():
            q = form.save(commit=False)

            cf = ChoiceForms(instance=q)

            if cf.is_valid():
                q.poll = poll

                q.save()
                cf.save()
                return redirect(
                    'poll-edit-questions',
                    poll.url
                )
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
            'questions': poll.questions.all(),
            'form': form,
            'choice_forms': cf
        }
    )


# TODO require permission
@login_required
def create(request):
    if request.method == 'POST':
        poll_form = forms.PollForm(request.POST)
        if poll_form.is_valid():

            np = poll_form.save(commit=False)

            if not np.url:
                np.url = np.url_from_name(np.name)

            np.save()

            return redirect('poll-edit-questions', np.url)

    else:
        poll_form = forms.PollForm()

    return render(
        request,
        'polls/poll/create.html',
        { 'poll_form': poll_form }
    )
