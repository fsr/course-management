from django.db import models
from django.contrib.auth.models import User
import random
import string


allowed_chars = string.ascii_letters + string.digits


class Poll(models.Model):
    name = models.CharField(max_length=200, unique=True)
    url = models.CharField(max_length=200, unique=True)


class Question(models.Model):
    question = models.CharField(max_length=500)
    poll = models.ForeignKey(Poll, related_name='questions')


class Choice(models.Model):
    value = models.CharField(max_length=100)
    poll = models.ForeignKey(Question, related_name='choices')


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
