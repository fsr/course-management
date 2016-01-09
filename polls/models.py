import random
import re
import string

from django.contrib.auth.models import User
from django.db import models

allowed_chars = string.ascii_letters + string.digits

ufn_regex = re.compile('[\w\d_-]+')


class Poll(models.Model):
    name = models.CharField(max_length=200, unique=True)
    url = models.CharField(max_length=200, unique=True)

    @staticmethod
    def url_from_name(name):
        return ''.join(
            m.group(0)
            for m in ufn_regex.finditer(
                name.replace(' ', '-')
            )
        )

    def questions_in_order(self):
        return self.questions.order_by('position')


class Question(models.Model):
    question = models.CharField(max_length=500)

    def choice_values(self):
        return map(lambda a: a.value, self.choices.all())

    def has_choices(self):
        return self.choices.count() > 0


def qlink_next_position():
    try:
        return QLink.objects.order_by('-position')[:1].get().position
    except QLink.DoesNotExist:
        return 1


class QLink(models.Model):
    required = models.BooleanField(default=True)
    question = models.ForeignKey(Question, related_name='values')
    poll = models.ForeignKey(Poll, related_name='questions')
    position = models.IntegerField(default=qlink_next_position)

    def html_question_id(self):
        return str(self.id)

    def has_choices(self):
        return self.question.has_choices()

    def submit_text_answer(self, text):
        QValue.objects.create(
                question=self,
                value=text
        )

    def increment_choice(self, choice):

        if not isinstance(choice, Choice):
            choice = Choice.objects.get(id=int(choice))

        c = self.counters.get_or_create(choice=choice, qlink=self)
        c.counter += 1
        c.save()

    def next_lower_to(self):
        return QLink.objects.filter(position__lt=self.position).order_by('-position')[:1].get()

    def next_higher_to(self):
        return QLink.objects.filter(position__gt=self.position).order_by('position')[:1].get()


class Choice(models.Model):
    value = models.CharField(max_length=100)
    question = models.ForeignKey(Question, related_name='choices')

    def html_input_id(self):
        return '-'.join(map(str, ('input', self.question.id, self.id)))


class Token(models.Model):
    LENGTH = 20
    token = models.CharField(max_length=LENGTH)
    poll = models.ForeignKey(Poll, related_name='tokens')
    used = models.BooleanField(default=False)

    @classmethod
    def generate(cls, poll, user=None):
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
    choice = models.ForeignKey(Choice, related_name='counters')
    counter = models.BigIntegerField(default=0)
    qlink = models.ForeignKey(QLink, related_name='counters')


class QValue(models.Model):
    question = models.ForeignKey(QLink, related_name='fulltext_answers')
    value = models.CharField(max_length=500)
