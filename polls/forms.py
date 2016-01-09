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
        """
        Initializer.

        Creates either an empty vote interface (data = None) or one with associated result data (data = some dict)

        :param link: associated question link.
        :param data: Data from post request
        """
        self.link = link
        self.data = data if data is None else data.get(self.html_name, None)
        self.errored = not self.is_valid() if data is not None else False

    @property
    def question(self):
        """
        Value of the associated question.

        :return: Question
        """
        return self.link.question.question

    def is_valid(self):
        """
        Is the input data valid?

        :return: True if data is valid, False otherwise (also if data=None)
        """
        return (not self.link.required) or self._data_is_valid()

    def _data_is_valid(self):
        return bool(self.data)

    def save(self):
        """
        Save the data from the post data.

        :return: None
        """
        if self.is_valid():
            return self._save()

    def _save(self):
        raise NotImplementedError

    @property
    def html_name(self):
        """
        Input field name to be used in HTML for this question.

        :return: HTML safe name string
        """
        if not hasattr(self, '_html_name_val'):
            self._html_name_val = "input-" + self.link.html_question_id()
        return self._html_name_val

    def error(self):
        """
        Error value for this question.
        """
        raise NotImplementedError


class ChoiceVoteInterface(AbstractVoteInterface):
    """
    Vote interface implementation for questions with choices.
    """
    is_choice = True

    class Choice:
        """
        Inner choice class. Represents a single choice
        """
        def __init__(self, interface, value, identifier, selected=False):
            """
            Initializer.

            :param interface: Associated interface.
            :param value: Associated value
            :param identifier: Associated id
            :param selected: Bool, is it selected?
            """
            self.interface = interface
            self.identifier = identifier
            self.db_value = value
            self.value = self.db_value.value
            self.selected = selected

        @property
        def count(self):
            """
            Current count for this choice.

            :return: int
            """
            try:
                c = ChoiceCounter.objects.get(choice=self.db_value, qlink=self.interface.link)
                return c.counter
            except ChoiceCounter.DoesNotExist:
                return 0

    def __init__(self, link: QLink, data=None):
        """
        Initializer.

        :param link: Associated link
        :param data: Associated data (optional)
        """
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
    """
    Vote interface implementation for a question with fulltext answers.
    """
    is_choice = False

    def _save(self):
        return QValue.objects.create(
                question=self.link,
                value=self.data
        )

    @property
    def value(self):
        """
        Directly associated value (from post request)

        :return: data
        """
        return self.data

    def error(self):
        return "This field is required."

    def get_values(self):
        """
        All associated submitted answers.

        :return: List-like collection of answers
        """
        return QValue.objects.filter(question=self.link)


class PollInterface:
    """
    Interface for interacting with a poll.
    """
    def __init__(self, poll: Poll, data=None):
        """
        Initilaizer.

        Either creates an empty interface for displaying the poll or a filled one
        (data != None) for saving and validating answers.

        :param poll: Associated poll
        :param data: Optional data from a post request
        """
        self.poll = poll
        self.data = data
        self.questions = list(map(self.make_vote_form, self.poll.questions_in_order().all()))

    def make_vote_form(self, qlink):
        """
        Create a single interface for a particular question link.

        :param qlink: associated question link
        :return: T extends AbstractVoteInterface
        """
        if qlink.has_choices():
            return ChoiceVoteInterface(qlink, self.data)
        else:
            return TextVoteInterface(qlink, self.data)

    def __iter__(self):
        """Yields questions."""
        yield from self.questions

    def is_valid(self):
        """
        Is the recieved data valid

        :return: True if valid, False otherwise
        """
        return reduce(lambda a, b: a and b.is_valid(), self.questions, True)

    def save(self):
        """
        Save all data from the request.
        """
        for q in self.questions:
            q.save()
