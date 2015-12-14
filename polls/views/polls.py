from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render
from django.forms import inlineformset_factory, formset_factory
from polls.models import Choice, Question
from polls import forms


def vote(request, poll_name):
    pass


def results(request, poll_name):
    pass

def view(request, poll_name):
    pass

# TODO require permission
@login_required
def create(request):
    FormSet = formset_factory(inlineformset_factory(Question, Choice, fields='__all__'))
    if request.method == 'POST':
        poll_form = forms.PollForm(request.POST)

        question_form = FormSet(request.POST)
    else:
        poll_form = forms.PollForm()
        question_form = FormSet()

    return render(
        request,
        'polls/poll/create.html',
        { 'form': poll_form
        , 'question_form': question_form }
    )
