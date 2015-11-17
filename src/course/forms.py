from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from course.models.schedule import WEEKDAYS, TIMESLOTS, Schedule, DateSlot, WeeklySlot
from course.models.subject import Subject
from course.models.course import Course

location_validator = RegexValidator(
    r'^.*$', # does absolutely nothing yet
    message='Invalid location name.'
)


SUBJECT_DISALLOWED_NAMES = ['new', 'overview']


subject_name_validator = RegexValidator(
    r'^(\w|[0-9_ -])+$',
    message='Invalid subject name.'
)


def subject_disallowed_names_validator(name):
    if name in SUBJECT_DISALLOWED_NAMES:
        raise ValidationError('Invalid subject name.')


def username_exists_validator(value):
    try:
        User.objects.get(username=value)

    except User.DoesNotExist:
        raise ValidationError('This username does not exist')


# class EditCourseForm(forms.Form):
#     description = forms.CharField(widget=forms.Textarea)
#     max_participants = forms.DecimalField(
#         min_value=1,
#         label="Maximum number of allowed participants",
#         help_text='Set a new limit for how many people can join the course. '
#                   'This does not unenroll any students. '
#                   'If the new limit is below the number of currently enrolled '
#                   'students it simply disables the option for joining the course.'
#     )


class DateForm(ModelForm):
    location = forms.CharField(max_length=100, validators=[location_validator])
    class Meta:
        model = DateSlot
        fields = ('date', 'location')



class WeeklySlotForm(forms.Form):
    location = forms.CharField(max_length=100, validators=[location_validator])
    class Meta:
        model = WeeklySlot
        field = ('weekday', 'timeslot')


class CourseForm(ModelForm):
    schedule_type = forms.ChoiceField(Schedule.TYPES)
    class Meta:
        model = Course
        fields = [
            'subject',
            'active',
            'description',
            'max_participants'
        ]
        help_texts = {
            'subject': 'Choose a subject for your course. ',
            'active': 'Choose whether people should be able to join this course '
                      'right now.',
            'description': 'A good description is half the battle. '
                           'You can use markdown for formatting.',
            'max_participants': 'How many people can join your course. (Can be changed later)'
        }
        labels = {
            'max_participants': 'Max nr. of participants'
        }


class AddTeacherForm(forms.Form):
    username = forms.CharField(
        help_text='Username of the person you want to be a teacher for this course',
        validators=[username_exists_validator]
    )


class NotifyCourseForm(forms.Form):
    subject = forms.CharField(
        min_length=1,
        help_text='This will become the subject field of the resulting email.'
    )
    content = forms.CharField(
        widget=forms.Textarea,
        help_text='This will be the content of the email. HTML is not allowed '
                  'and any html tags will be removed.'
    )
    show_sender = forms.BooleanField(
        initial=False,
        required=False,
        help_text='Whether to set the email sender to your email address or not.'
    )


class SubjectForm(ModelForm):
    name = forms.CharField(
        validators=[subject_name_validator,
                    subject_disallowed_names_validator],
        help_text=
            'Name of the subject, also decides its url. '
            'Allowed characters are word characters, numbers, spaces, '
            '\'-\' and \'_\' and it cannot be any of '
            + ', '.join(map(lambda a: '\'' + a + '\'', SUBJECT_DISALLOWED_NAMES)) + '.'

    )
    class Meta:
        model = Subject
        fields = [
            'name',
            'description'
        ]
