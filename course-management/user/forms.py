from django import forms
from django.core.validators import RegexValidator, validate_email
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

from user.models import UserInformation, User
from django.core.exceptions import ValidationError
from util import html_clean


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


class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + \
            ('email', 'first_name', 'last_name')
        labels = {
            'email': _('E-Mail address'),
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'username': _('Username')
        }
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
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'email': _("Mail address")
        }
        help_texts = {
            'first_name': _('First part of your public name, which should be your genuine first name. '
                            'If you become a teacher this will be visible to any site visitor. '
                            'Can be modified later.'),
            'last_name': _('Second part of your public name, which should be your genuine familyname. '
                           'If you become a teacher this will be visible to any site visitor. '
                           'Can be modified later'),
            'email': _('Your mail address'),
        }


class UserInformationForm(ModelForm):
    description = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = UserInformation
        fields = ('public_profile', 'description', 'accepted_privacy_policy')
        labels = {
            'public_profile': _('Public Profile'),
            'description': _('Description'),
            'accepted_privacy_policy': _('Privacy Policy')
        }
        help_texts = {
            'description': _('Tell something about yourself. (Markdown enabled) Links are allowed.'),
            'accepted_privacy_policy': _('You have read our <a href="/privacy-policy/" style="color:#9ACC00 !important;">Privacy Policy</a> and consent to it.')
        }


class ContactForm(forms.Form):
    subject = forms.CharField(help_text=_(
        'This will become the subject field of the resulting email.'))
    content = forms.CharField(
        widget=forms.Textarea,
        help_text=_('This will be the content of the email. HTML is not allowed '
                    'and any html tags will be removed.')
    )

    def clean(self):
        super().clean()
        self.subject = html_clean.clean_all(self.data['subject'])
        self.content = html_clean.clean_all(self.data['content'])


class PrivacyAgreementForm(ModelForm):
    class Meta:
        model = UserInformation
        fields = ('accepted_privacy_policy',)
        labels = {
            'accepted_privacy_policy': ''
        }
        help_texts = {
            'accepted_privacy_policy': _('I have read the Privacy Policy and consent to it.')
        }
