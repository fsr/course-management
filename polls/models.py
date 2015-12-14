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


class Question(models.Model):
    question = models.CharField(max_length=500)
    poll = models.ForeignKey(Poll, related_name='questions')

    def html_question_id(self):
        return self.id

    def has_choices(self):
        return self.choices.count() > 0


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
    user = models.ForeignKey(User, null=True)

    @classmethod
    def generate(cls, poll, user=None):
        token = random.sample(allowed_chars, cls.LENGTH)
        try:
            cls.objects.get(token=token, poll=poll)
            return cls.generate(poll, user)
        except cls.DoesNotExist:
            return cls.objects.create(
                token=token,
                poll=poll,
                user=None
            )