from functools import reduce

from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from polls.models import Poll, Choice, Question, ufn_regex, QLink, ChoiceCounter, QValue


class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = '__all__'


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ('question',)


class PollForm(ModelForm):
    url = forms.CharField(
            required=False,
            help_text=_('A url to use for this poll (optional)'),
            validators=[RegexValidator(ufn_regex)]
    )

    class Meta:
        model = Poll
        fields = ('name', 'url')


class AbstractVoteInterface:
    def __init__(self, link: QLink, data=None):
        self.link = link
        self.data = data

    def is_valid(self):
        return (not self.link.required) or self._data_is_valid()

    def _data_is_valid(self):
        return bool(self.data)

    def save(self):
        if self.is_valid():
            return self._save()
        else:
            return None

    def _save(self):
        raise NotImplementedError


class ChoiceVoteInterface(AbstractVoteInterface):
    def __init__(self, link: QLink, data=None):
        super().__init__(link, data)
        try:
            self.choice = Choice.objects.get(value=data, question=link.question)
        except Choice.DoesNotExist:
            self.choice = None

    def _data_is_valid(self):
        return self.choice is not None and super()._data_is_valid()

    def _save(self):
        counter, _ = ChoiceCounter.objects.get_or_create({'counter': 0}, choice=self.choice, qlink=self.link)
        counter.counter += 1
        counter.save()
        return counter

    def get_count(self):
        try:
            c = ChoiceCounter.objects.get(choice=self.choice, qlink=self.link)
            return c.counter
        except ChoiceCounter.DoesNotExist:
            return 0


class TextVoteInterface(AbstractVoteInterface):
    def _save(self):
        return QValue.objects.create(
                question=self.link,
                value=self.data
        )


class VoteInterface:
    def __init__(self, poll: Poll, data=None):
        self.poll = poll
        self.data = data
        self.questions = list(map(self.make_vote_form, self.poll.questions))

    def make_vote_form(self, qlink):
        if qlink.has_choices():
            return ChoiceVoteInterface(qlink, self.data.get(qlink.html_question_id(), None))
        else:
            return TextVoteInterface(qlink, self.data.get(qlink.html_question_id(), None))

    def __iter__(self):
        yield from self.questions

    def is_valid(self):
        return reduce(lambda a, b: a and b.is_valid(), self.questions, True)

    def save(self):
        for q in self.questions:
            q.save()
