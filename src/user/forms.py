from django import forms
from django.core.validators import RegexValidator

from user.models import Faculty, Student


def get_faculties():
    return map(lambda fak: (fak.id, fak.name), Faculty.objects.all())


name_validator = RegexValidator(
    r'^\w+((-| )\w+)*$',
    message='Names should start with capital letters, only contain regular'
            ' characters and be separated with spaces or dashes.'
)
s_number_validator = RegexValidator(
    r'^s?\d{7}$',
    message='S numbers can start with an \'s\' and otherwise consist of a '
            'string of seven digits.'
)
def s_number_existence_validator(number):
    try:
        User.objects.get(username=number)
    except User.DoesNotExist:
        raise ValidationError('This s-number is already taken')


class LoginForm(forms.Form):
    username = forms.CharField(
        help_text='Your s-number.'
    )
    password = forms.PasswordInput()


class RegistrationForm(forms.Form):
    first_name = forms.CharField(
        validators=[name_validator],
        help_text='First part of your public name, which should be your genuine first name. '
                  'If you become a teacher this will be visible to any site visitor. '
                  'Can be modified later.'
    )
    family_name = forms.CharField(
        validators=[name_validator],
        help_text='Second part of your public name, which should be your genuine familyname. '
                  'If you become a teacher this will be visible to any site visitor. '
                  'Can be modified later'
    )
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)
    password_repeat = forms.CharField(min_length=8, widget=forms.PasswordInput)
    s_number = forms.CharField(
        min_length=6,
        validators=[s_number_validator, s_number_existence_validator],
        help_text='The s-number as assigned by the university. This will become your (private) username for this site. '
                  'The verification email will be sent to the address associated with this s-number. '
                  'Cannot be modified later.'
    )
    faculty = forms.ChoiceField(
        choices=get_faculties,
        help_text='The faculty at which you are enrolled. (Used for crediting purposes) Can be modified later.'
    )


class ModifyUserForm(forms.Form):
    first_name = forms.CharField(
        validators=[name_validator],
        help_text='First part of your public name, which should be your genuine first name. '
                  'If you become a teacher this will be visible to any site visitor.'
    )
    last_name = forms.CharField(
        required=False,
        validators=[name_validator],
        help_text='Second part of your public name, which should be your genuine familyname. '
                  'If you become a teacher this will be visible to any site visitor.'
    )
    email = forms.EmailField()
    faculty = forms.ChoiceField(
        choices=get_faculties,
        help_text='The faculty at which you are enrolled. (Used for crediting purposes)'
    )
    public_profile = forms.BooleanField(
        required=False,
        initial=False,
        help_text='Whether some of your data should be visible to others. Visible data would be first_name, last_name, '
                  'the courses you teach and the description you provide below.'
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea,
        help_text='Here you can provide some information about yourself. '
                  'You can use markdown formatted text to do so. '
    )
