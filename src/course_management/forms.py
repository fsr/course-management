from django import forms
from django.core.validators import RegexValidator
from course_management.models.schedule import WEEKDAYS, TIMESLOTS


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