from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from course.models.schedule import Schedule, DateSlot, WeeklySlot
from course.models.subject import Subject
from course.models.course import Course
from user.forms import AbstractContactForm


location_validator = RegexValidator(
    r'^.*$', # does absolutely nothing yet
    message=_('Invalid location name.')
)


SUBJECT_DISALLOWED_NAMES = ['new', 'overview']


subject_name_validator = RegexValidator(
    r'^(\w|[0-9_ -])+$',
    message=_('Invalid subject name.')
)


def subject_disallowed_names_validator(name):
    if name in SUBJECT_DISALLOWED_NAMES:
        raise ValidationError(_('Invalid subject name.'))


def username_exists_validator(value):
    try:
        User.objects.get(username=value)

    except User.DoesNotExist:
        raise ValidationError(_('Requested username does not exist.'))


class DateForm(ModelForm):
    location = forms.CharField(max_length=100, validators=[location_validator])

    class Meta:
        model = DateSlot
        fields = ('date', 'location')


class WeeklySlotForm(ModelForm):
    location = forms.CharField(max_length=100, validators=[location_validator])

    class Meta:
        model = WeeklySlot
        fields = ('weekday', 'timeslot')


class CourseForm(ModelForm):
    schedule_type = forms.ChoiceField(Schedule.TYPES)

    class Meta:
        model = Course
        widgets = {
            'start_time': forms.DateInput(attrs={'class': 'datepicker'}),
            'end_time': forms.DateInput(attrs={'class': 'datepicker'}),
        }

        fields = [
            'subject',
            'active',
            'description',
            'max_participants',
            'archiving',
            'student_only',
            'start_time',
            'end_time'
        ]
        help_texts = {
            'subject': _('Choose a subject for your course. '),
            'active':   _(
                        'Choose whether people should be able to join this course '
                        'right now.'
                        ),
            'description':  _(
                            'A good description is half the battle. '
                            'You can use markdown for formatting.'
                            ),
            'max_participants': _('How many people can join your course. (Can be changed later)'),
            'student_only': _('Should your course only be available to students?'),
            'start_time': _('The course starts on that day.'),
            'end_time': _('The course will end at that day.')
        }
        labels = {
            'max_participants': _('Max nr. of participants'),
            'start_time': _('Begin'),
            'end_time': _('End')
        }


class AddTeacherForm(forms.Form):
    username = forms.CharField(
        help_text=_('Username of the person you want to be a teacher for this course'),
        validators=[username_exists_validator]
    )


class NotifyCourseForm(AbstractContactForm):
    show_sender = forms.BooleanField(
        initial=False,
        required=False,
        help_text=_('Whether to set the email sender to your email address or not.')
    )


class SubjectForm(ModelForm):
    name = forms.CharField(
        validators=[subject_name_validator,
                    subject_disallowed_names_validator],
        help_text=_(
            'Name of the subject, also decides its url. '
            'Allowed characters are word characters, numbers, spaces, '
            '\'-\' and \'_\' and it cannot be any of '
            + ', ').join(map(lambda a: '\'' + a + '\'', SUBJECT_DISALLOWED_NAMES)) + '.'

    )
    class Meta:
        model = Subject
        fields = [
            'name',
            'description_en',
            'description_de',
        ]
