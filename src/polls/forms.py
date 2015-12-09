from django import forms
from django.forms import ModelForm, modelformset_factory, formset_factory



from polls.models import Poll, Choice, Question


class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = '__all__'


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ('question',)


class PollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ('name',)
