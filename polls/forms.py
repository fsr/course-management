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
    is_choice = NotImplemented

    def __init__(self, link: QLink, data=None):
        self.link = link
        self.data = data if data is None else data.get(self.html_name(), None)
        self.errored = not self.is_valid() if data is not None else False

    def question(self):
        return self.link.question.question

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

    def html_name(self):
        return "input-" + self.link.html_question_id()

    def error(self):
        raise NotImplementedError


class ChoiceVoteInterface(AbstractVoteInterface):
    is_choice = True

    class Choice:
        def __init__(self, interface, value, identifier, selected=False):
            self.interface = interface
            self.identifier = identifier
            self.db_value = value
            self.value = self.db_value.value
            self.selected = selected

        def get_count(self):
            try:
                c = ChoiceCounter.objects.get(choice=self.db_value, qlink=self.interface.link)
                return c.counter
            except ChoiceCounter.DoesNotExist:
                return 0

    def __init__(self, link: QLink, data=None):
        super().__init__(link, data)
        if data is not None:
            try:
                self.data = Choice.objects.get(
                        id=self.data,
                        question=link.question
                )
            except Choice.DoesNotExist:
                self.data = None
        self.choices = [
            self.Choice(self, c, c.id, selected=c == self.data)
            for c in self.link.question.choices.all()
            ]

    def _data_is_valid(self):
        return self.data is not None

    def _save(self):
        counter, _ = ChoiceCounter.objects.get_or_create({'counter': 0}, choice=self.data, qlink=self.link)
        counter.counter += 1
        counter.save()
        return counter

    def error(self):
        return "This field is required."


class TextVoteInterface(AbstractVoteInterface):
    is_choice = False

    def _save(self):
        return QValue.objects.create(
                question=self.link,
                value=self.data
        )

    def value(self):
        return self.data

    def error(self):
        return "This field is required."

    def get_values(self):
        return QValue.objects.filter(question=self.link)


class VoteInterface:
    def __init__(self, poll: Poll, data=None):
        self.poll = poll
        self.data = data
        self.questions = list(map(self.make_vote_form, self.poll.questions.all()))

    def make_vote_form(self, qlink):
        if qlink.has_choices():
            return ChoiceVoteInterface(qlink, self.data)
        else:
            return TextVoteInterface(qlink, self.data)

    def __iter__(self):
        yield from self.questions

    def is_valid(self):
        return reduce(lambda a, b: a and b.is_valid(), self.questions, True)

    def save(self):
        for q in self.questions:
            q.save()
