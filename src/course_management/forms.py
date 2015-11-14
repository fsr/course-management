from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from course_management.models.schedule import WEEKDAYS, TIMESLOTS, Schedule
from course_management.models.subject import Subject

location_validator = RegexValidator(
    r'^.*$', # does absolutely nothing yet
    message='Invalid location name.'
)


def username_exists_validator(value):
    try:
        User.objects.get(username=value)

    except User.DoesNotExist:
        raise ValidationError('This username does not exist')


class EditCourseForm(forms.Form):
    active = forms.BooleanField(initial=False)
    description = forms.CharField(widget=forms.Textarea)
    max_participants = forms.DecimalField(min_value=1, label="Maximum number of allowed participants")


class AddDateForm(forms.Form):
    date = forms.DateTimeField()
    location = forms.CharField(validators=[location_validator])


class AddWeeklySlotForm(forms.Form):
    weekday = forms.ChoiceField(WEEKDAYS)
    timeslot = forms.ChoiceField(TIMESLOTS)
    location = forms.CharField(validators=[location_validator])


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
        help_text='A good description is half the battle. You can use markdown for formatting.',
        initial='# My course\n\nWe will explore the universe.\n\n## Materials\n\n- a spaceship\n- lots of courage'
    )
    max_participants = forms.DecimalField(
        min_value=1,
        initial=30,
        label='Max nr. of participants',
        help_text='How many people can join your course. (Can be changed later)'
    )


class AddTeacherForm(forms.Form):
    username = forms.CharField(
        help_text='Username of the person you want to be a teacher for this course',
        validators=[username_exists_validator]
    )
