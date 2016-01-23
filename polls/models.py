import random
import re
import string

from django.contrib.auth.models import User
from django.db import models

from guardian.models import UserObjectPermission

allowed_chars = string.ascii_letters + string.digits

ufn_regex = re.compile('[\w\d_-]+')


class Poll(models.Model):
    """
    A poll.

    Harbors a list of questions and links to results (by proxy).
    """
    name = models.CharField(max_length=200, unique=True)
    url = models.CharField(max_length=200, unique=True)

    @staticmethod
    def url_from_name(name):
        """
        A sanitized version of the name, fit for a url.
        """
        return ''.join(
            m.group(0)
            for m in ufn_regex.finditer(
                name.replace(' ', '-')
            )
        )

    def questions_in_order(self):
        """
        Questions in this poll sorted by position.
        """
        return self.questions.order_by('position')

    def is_owner(self, student):
        """
        Whether student is the owner of this poll. This corresponds to change
        and delete permissions as they are automatically assigned upon creation
        """
        return student.user.has_perm("polls.change_poll", self) \
                and student.user.has_perm("polls.delete_poll", self)


class Question(models.Model):
    """
    A question template. Reusable, has no results associated directly.
    """
    question = models.CharField(max_length=500)

    def choice_values(self):
        """
        The values of the associated choices.
        """
        return map(lambda a: a.value, self.choices.all())

    def has_choices(self):
        """
        Whether this question is free text or choices.
        """
        return self.choices.count() > 0


def qlink_next_position():
    """
    Next free 'position' value.
    """
    try:
        return QLink.objects.order_by('-position')[:1].get().position + 1
    except QLink.DoesNotExist:
        return 1


class QLink(models.Model):
    """
    Associates a question with a poll and it's results for the particular poll.
    """
    required = models.BooleanField(default=True)
    question = models.ForeignKey(Question, related_name='values')
    poll = models.ForeignKey(Poll, related_name='questions')
    position = models.IntegerField(default=qlink_next_position)

    def html_question_id(self):
        """
        Id to be used for this link in HTML.
        """
        return str(self.id)

    def has_choices(self):
        """
        Whether the question for this link is free text or has choices.
        """
        return self.question.has_choices()

    def submit_text_answer(self, text):
        """
        Submit a new text answer for this Question.
        :param text: Text content for the answer
        :return self
        """
        QValue.objects.create(
                question=self,
                value=text
        )
        return self

    def increment_choice(self, choice):
        """
        Increment the value for a choice.

        :param choice: Choice to increment value for
        :return: new counter value
        """
        if not isinstance(choice, Choice):
            choice = Choice.objects.get(id=int(choice))

        c = self.counters.get_or_create(choice=choice, qlink=self)
        c.counter += 1
        c.save()
        return c.counter

    def next_lower_to(self):
        """
        The closest link with a greater position value

        :return: close link
        """
        return self.__class__.objects.filter(position__gt=self.position, poll=self.poll).order_by('position')[:1].get()

    def next_higher_to(self):
        """
        The closest link with a smaller position value

        :return: close link
        """
        return self.__class__.objects.filter(position__lt=self.position, poll=self.poll).order_by('-position')[:1].get()


class Choice(models.Model):
    """
    The value for a (single) choice
    """
    value = models.CharField(max_length=100)
    question = models.ForeignKey(Question, related_name='choices')

    @property
    def html_input_id(self):
        """
        Id to be used for the html input for this choice.

        :return:
        """
        if not hasattr(self, '_html_input_id_val'):
            self._html_input_id_val = '-'.join(map(str, ('input', self.question.id, self.id)))
        return self._html_input_id_val


class Token(models.Model):
    """
    Token that allows participation in a poll.
    """
    LENGTH = 20
    token = models.CharField(max_length=LENGTH)
    poll = models.ForeignKey(Poll, related_name='tokens')
    used = models.BooleanField(default=False)

    @classmethod
    def generate(cls, poll, user=None):
        """
        Generate a new token for a particular poll.

        :param poll: Poll which the token belongs to.
        :param user: User associated with the token.
        :return: new token object
        """
        token = random.sample(allowed_chars, cls.LENGTH)
        try:
            cls.objects.get(token=token, poll=poll)
            return cls.generate(poll, user)
        except cls.DoesNotExist:
            return cls.objects.create(
                token=token,
                    poll=poll
            )


class ChoiceCounter(models.Model):
    """
    Counter for a single choice for a particular poll.
    """
    choice = models.ForeignKey(Choice, related_name='counters')
    counter = models.BigIntegerField(default=0)
    qlink = models.ForeignKey(QLink, related_name='counters')


class QValue(models.Model):
    """
    A fulltext answer for a particular question, for a particular poll.
    """
    question = models.ForeignKey(QLink, related_name='fulltext_answers')
    value = models.CharField(max_length=500)
