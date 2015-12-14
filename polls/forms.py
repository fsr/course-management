from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from polls.models import Poll, Choice, Question, ufn_regex


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
