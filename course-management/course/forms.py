from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from course.models.course import Course
from course.models.schedule import Schedule, DateSlot, WeeklySlot
from course.models.subject import Subject
from course.models.news import News
from user.forms import ContactForm

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
    """
    Make sure the subject has no reserved name, otherwise its page won't be reachable.

    :param name: name to test
    """
    if name in SUBJECT_DISALLOWED_NAMES:
        raise ValidationError(_('Invalid subject name.'))


def username_exists_validator(value):
    """
    Make sure a username exists.

    :param value: name
    """
    try:
        User.objects.get(username=value)

    except User.DoesNotExist:
        raise ValidationError(_('Requested username does not exist.'))


class DateForm(ModelForm):
    location = forms.CharField(max_length=100, validators=[location_validator])

    class Meta:
        model = DateSlot
        fields = ('date', 'location')

    date = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M'),
        input_formats=['%Y-%m-%dT%H:%M'])


class WeeklySlotForm(ModelForm):
    location = forms.CharField(max_length=100, validators=[location_validator])

    class Meta:
        model = WeeklySlot
        fields = ('weekday', 'timeslot', 'location')


class CourseForm(ModelForm):
    schedule_type = forms.ChoiceField(choices=Schedule.TYPES)

    class Meta:
        model = Course
        fields = [
            'subject',
            'active',
            'visible',
            'description',
            'max_participants',
            'archiving',
            'start_time',
            'end_time',
            'schedule_type'
        ]
        help_texts = {
            'subject': _('Choose a subject for your course. '),
            'active':   _(
                        'Choose whether people should be able to join this course '
                        'right now.'
                        ),
            'visible': _('Choose whether people should see the course even if its not active'),
            'description':  _(
                            'A good description is half the battle. '
                            'You can use markdown for formatting.'
                            ),
            'max_participants': _('How many people can join your course. (Can be changed later)'),
            'start_time': _('The course starts on that day.'),
            'end_time': _('The course will end at that day.')
        }
        labels = {
            'max_participants': _('Max nr. of participants'),
            'start_time': _('Begin'),
            'end_time': _('End')
        }

    start_time = forms.DateField(
        widget=forms.DateInput(format='%d.%m.%Y'),
        input_formats=['%d.%m.%Y', '%Y-%m-%d'])
    end_time = forms.DateField(
        widget=forms.DateInput(format=('%d.%m.%Y')),
        input_formats=['%d.%m.%Y', '%Y-%m-%d'])


class AddTeacherForm(forms.Form):
    username = forms.CharField(
        help_text=_('Username of the person you want to be a teacher for this course'),
        validators=[username_exists_validator]
    )


class NotifyCourseForm(ContactForm):
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

class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = [
            'headline',
            'entry'
        ]
