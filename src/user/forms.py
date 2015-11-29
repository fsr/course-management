from django import forms
from django.core.validators import RegexValidator, EmailValidator
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from user.models import Faculty, UserInformation, StudentInformation, User
from django.core.exceptions import ValidationError
from util import html_clean


def get_faculties():
    return map(lambda fak: (fak.id, fak.name), Faculty.objects.all())


def faculties_or_empty():
    yield ('', 'none')
    yield from get_faculties()


name_validator = RegexValidator(
    r'^\w+((-| )\w+)*$',
    message=_('Names should start with capital letters, only contain regular'
            ' characters and be separated with spaces or dashes.')
)
s_number_validator = RegexValidator(
    r'^s?\d{7}$',
    message=_('S numbers can start with an \'s\' and otherwise consist of a '
            'string of seven digits.')
)
def username_existence_validator(number):
    try:
        User.objects.get(username=number)
    except User.DoesNotExist:
        return
    raise ValidationError(_('This s-number is already taken'))

def s_number_existence_validator(number):
    try:
        StudentInformation.objects.get(s_number=number)
    except StudentInformation.DoesNotExist:
        return
    raise ValidationError('This s-number is already taken')


class LoginForm(forms.Form):
    username = forms.CharField(
        help_text=_('Your s-number.')
    )
    password = forms.PasswordInput()
    

class RegistrationForm(forms.Form):
    username = forms.CharField(validators=[username_existence_validator])
    first_name = forms.CharField(
        validators=[name_validator],
        help_text=_('First part of your public name, which should be your genuine first name. '
                  'If you become a teacher this will be visible to any site visitor. '
                  'Can be modified later.')
    )
    family_name = forms.CharField(
        validators=[name_validator],
        help_text=_('Second part of your public name, which should be your genuine familyname. '
                  'If you become a teacher this will be visible to any site visitor. '
                  'Can be modified later')
    )
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)
    password_repeat = forms.CharField(min_length=8, widget=forms.PasswordInput)
    email = forms.CharField(validators=[EmailValidator])
    s_number = forms.CharField(
        min_length=6,
        validators=[s_number_validator, s_number_existence_validator],
        help_text=_('The s-number as assigned by the university. This will become your (private) username for this site. '
                  'The verification email will be sent to the address associated with this s-number. '
                  'Cannot be modified later.'),
        required=False
    )
    faculty = forms.ChoiceField(
        choices=faculties_or_empty,
        help_text=_('The faculty at which you are enrolled. (Used for crediting purposes) Can be modified later.'),
        required=False
    )


class ModifyUserForm(forms.Form):
    first_name = forms.CharField(
        validators=[name_validator],
        help_text=_('First part of your public name, which should be your genuine first name. '
                  'If you become a teacher this will be visible to any site visitor. '
                  'Can be modified later.')
    )
    last_name = forms.CharField(
        required=False,
        validators=[name_validator],
        help_text=_('Second part of your public name, which should be your genuine familyname. '
                  'If you become a teacher this will be visible to any site visitor. '
                  'Can be modified later')
    )
    email = forms.EmailField()
    faculty = forms.ChoiceField(
        choices=faculties_or_empty,
        help_text=_('The faculty at which you are enrolled. (Used for crediting purposes) Can be modified later.')
    )
    public_profile = forms.BooleanField(
        required=False,
        initial=False,
        help_text=_('Whether some of your data should be visible to others. Visible data would be first_name, last_name, '
                  'the courses you teach and the description you provide below.')
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea,
        help_text=_('Here you can provide some information about yourself. '
                  'You can use markdown formatted text to do so. ')
    )


class AbstractContactForm(forms.Form):
    subject = forms.CharField(help_text=_('This will become the subject field of the resulting email.'))
    content = forms.CharField(
        widget=forms.Textarea,
        help_text=_('This will be the content of the email. HTML is not allowed '
                          'and any html tags will be removed.')
    )

    def clean(self):
        super().clean()
        self.subject = html_clean.clean_all(self.subject)
        self.content = html_clean.clean_all(self.content)


class ContactForm(AbstractContactForm):
    sender = forms.CharField(
        help_text=_('An email address where the recipient may reach you.'),
        validators=[EmailValidator]
    )


class StudentVerificationForm(ModelForm):
    class Meta:
        model = StudentInformation
        fields = [
            's_number',
            'faculty'
        ]