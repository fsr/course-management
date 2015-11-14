from django import forms
from django.core.validators import RegexValidator

from user.models import Faculty


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


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.PasswordInput()


class RegistrationForm(forms.Form):
    first_name = forms.CharField(validators=[name_validator])
    family_name = forms.CharField(validators=[name_validator])
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)
    password_repeat = forms.CharField(min_length=8, widget=forms.PasswordInput)
    s_number = forms.CharField(min_length=6, validators=[s_number_validator])
    faculty = forms.ChoiceField(choices=get_faculties)


class ModifyUserForm(forms.Form):
    first_name = forms.CharField(required=False, validators=[name_validator])
    last_name = forms.CharField(required=False, validators=[name_validator])
    email = forms.EmailField(required=False)
    faculty = forms.ChoiceField(choices=get_faculties, required=False)
