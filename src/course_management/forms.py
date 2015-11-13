from django import forms
from django.core.validators import RegexValidator
from course_management.models.schedule import WEEKDAYS, TIMESLOTS, Schedule
from course_management.models.subject import Subject

place_validator = RegexValidator(
    r'^.*$', # does absolutely nothing yet
    message='Invalid place name.'
)


class EditCourseForm(forms.Form):
    active = forms.BooleanField(initial=False)
    description = forms.CharField(widget=forms.Textarea)
    max_participants = forms.DecimalField(min_value=1, label="Maximum number of allowed participants")


class AddDateForm(forms.Form):
    date = forms.DateTimeField()
    place = forms.CharField(validators=[place_validator])


class AddWeeklySlotForm(forms.Form):
    weekday = forms.ChoiceField(WEEKDAYS)
    timeslot = forms.ChoiceField(TIMESLOTS)
    place = forms.CharField(validators=[place_validator])


class CreateCourseForm(forms.Form):
    subject = forms.ChoiceField(
        lambda: map(lambda s: (s.id, s.name), Subject.objects.all()),
        help_text='Choose a subject for your course. '
                  'Beware that this choice may not be changed later'
    )
    schedule = forms.ChoiceField(Schedule.TYPES)
    active = forms.BooleanField(
        initial=False,
        help_text='Choose whether people should be able to join this course right now.'
    )
    description = forms.CharField(
        widget=forms.Textarea,
        help_text='A good description is half the battle. You can use markdown for formatting.'
    )
    max_participants = forms.DecimalField(
        min_value=1,
        label='Max nr. of participants',
        help_text='How many people can join your course. (Can be changed later)'
    )
