from django import forms
from course_management.models import faculty


get_faculties = lambda : map(lambda fak: (fak.id, fak.name), faculty.Faculty.objects.all())


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.PasswordInput()


class RegistrationForm(forms.Form):
    first_name = forms.CharField()
    family_name = forms.CharField()
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)
    password_repeat = forms.CharField(min_length=8, widget=forms.PasswordInput)
    s_number = forms.CharField(min_length=6)
    email = forms.EmailField()
    faculty = forms.ChoiceField(choices=get_faculties)


class ModifyUserForm(forms.Form):
    first_name = forms.CharField(required=False)
    family_name = forms.CharField(required=False)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput, required=False)
    password_repeat = forms.CharField(min_length=8, widget=forms.PasswordInput, required=False)
    email = forms.EmailField(required=False)
    faculty = forms.ChoiceField(choices=get_faculties, required=False)
