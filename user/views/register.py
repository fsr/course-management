import random
import string

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.translation import ugettext as _

from user import mailsettings
from user.forms import StudentVerificationForm, UserInformationForm, StudentInformationForm, UserForm
from user.models import UserInformation, Activation, ACTIVATION_TYPES


from re_captcha.decorators import re_captcha_verify


@re_captcha_verify
def register(request):

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        userinformation_form = UserInformationForm(request.POST)
        studentinformation_form = StudentInformationForm(request.POST)
        if (    user_form.is_valid()
            and userinformation_form.is_valid()
            and ( studentinformation_form.is_valid()
                 or (    not studentinformation_form.cleaned_data.get('faculty')
                     and not studentinformation_form.cleaned_data.get('s_number')))):

            created_user = user_form.save()

            acc = []

            if (    studentinformation_form.cleaned_data.get('faculty')
                and studentinformation_form.cleaned_data.get('s_number')):

                created_student_information = studentinformation_form.save(commit=False)

                created_student_information.user = created_user

                created_student_information.save()

                zih_mail = created_student_information.make_zih_mail()
                verification_mail(created_user, 'student', zih_mail)

                acc.append(zih_mail)

                if created_user.email != zih_mail:
                    verification_mail(created_user, 'email', created_user.email)
                    acc.append(created_user.email)

            else:
                created_user_information = userinformation_form.save(commit=False)

                created_user_information.user = created_user

                created_user_information.save()

                verification_mail(created_user, 'email', created_user.email)

                acc.append(created_user.email)

            return render(
                request,
                'registration/success.html',
                {
                    'title': _('Registration successfull'),
                    'acc': acc
                }
            )
        else:
            print('validation failed')
    else:
        user_form = UserForm()
        userinformation_form = UserInformationForm()
        studentinformation_form = StudentInformationForm()

    return render(
        request,
        'registration/register.html',
        {
            'title': _('Registration'),
            'user_form': user_form,
            'userinformation_form': userinformation_form,
            'studentinformation_form': studentinformation_form
        }
    )


def generateToken(size=50, chars=None):
    chars = (chars
        if chars is not None
        else string.ascii_uppercase + string.digits + string.ascii_lowercase
    )
    return ''.join(random.sample(chars, size))


def verification_mail(user, type_, email):
    type_ = type_.lower()
    type_val = ACTIVATION_TYPES[type_]

    user_token = generateToken()
    Activation.objects.create(user=user, token=user_token, type=type_val)
    activateurl = reverse('verify', args=[type_]) + '?token=' + user_token
    # print(activateurl)
    with open('res/registrationmail.txt') as f:
        message = f.read()
        message = message.format(
            user=user.first_name,
            url=activateurl
        )

    userinf = user.userinformation
    # print(message)
    send_mail(
        _('Your {} verification at the iFSR course enrollment system.'.format(type_)),
        message,
        mailsettings.sender,
        [email],
        mailsettings.auth_user,
        mailsettings.auth_pass
    )
    # print(user_token)
