from django import forms
from django.core.validators import RegexValidator, EmailValidator
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

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
    raise ValidationError(_('This username is already taken'))


def s_number_existence_validator(number):
    try:
        StudentInformation.objects.get(s_number=number)
    except StudentInformation.DoesNotExist:
        return
    raise ValidationError('This s-number is already taken')


class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')
        help_texts = {
            'email': _('An email adress where you can be reached. '
                       'The verification mail will be sent to this adress.'),
            'first_name': _('First part of your public name, which should be your genuine first name. '
                            'If you become a teacher this will be visible to any site visitor. '
                            'Can be modified later.'),
            'last_name': _('Second part of your public name, which should be your genuine familyname. '
                           'If you become a teacher this will be visible to any site visitor. '
                           'Can be modified later'),
            'username': _('Unique username. Used for login. (cannot be changed later).')
        }


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        help_texts = {
            'first_name': _('First part of your public name, which should be your genuine first name. '
                            'If you become a teacher this will be visible to any site visitor. '
                            'Can be modified later.'),
            'last_name': _('Second part of your public name, which should be your genuine familyname. '
                           'If you become a teacher this will be visible to any site visitor. '
                           'Can be modified later'),
        }


class UserInformationForm(ModelForm):
    description = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = UserInformation
        fields = ('public_profile', 'description')


class StudentInformationForm(ModelForm):
    class Meta:
        model = StudentInformation
        fields = ('s_number', 'faculty')
        help_texts = {
            's_number': _('The s-number as assigned by the university. '
                          'The student verification email will be sent to the address associated with this s-number. '
                          'Cannot be modified later.'),
            'faculty': _('The faculty at which you are enrolled. (Used for crediting purposes) Can be modified later.')
        }


class AbstractContactForm(forms.Form):
    subject = forms.CharField(help_text=_('This will become the subject field of the resulting email.'))
    content = forms.CharField(
        widget=forms.Textarea,
        help_text=_('This will be the content of the email. HTML is not allowed '
                    'and any html tags will be removed.')
    )

    def clean(self):
        super().clean()
        self.subject = html_clean.clean_all(self.data['subject'])
        self.content = html_clean.clean_all(self.data['content'])


class ContactForm(AbstractContactForm):
    sender = forms.CharField(
        help_text=_('An email address where the recipient may reach you.'),
        validators=[EmailValidator]
    )


class StudentVerificationForm(ModelForm):
    class Meta:
        model = StudentInformation
        fields = ('s_number', 'faculty')
