from django import forms


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
