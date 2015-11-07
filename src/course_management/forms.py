from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.PasswordInput()

class RegistrationForm(forms.Form):
    first_name = forms.CharField()
    family_name = forms.CharField()
    password = forms.PasswordInput()
    password_repeat = forms.PasswordInput()
    s_number = forms.CharField(min_lenght=6)
    email = forms.EmailInput()
