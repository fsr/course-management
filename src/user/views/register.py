import random
import string

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.translation import ugettext as _

from user import mailsettings
from user.forms import StudentVerificationForm, UserInformationForm, StudentInformationForm, UserForm
from user.models import UserInformation, Activation

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
                 or (    not studentinformation_form.faculty
                     and not studentinformation_form.s_number))):

            created_user = user_form.save()

            created_user_information = userinformation_form.save(commit=False)

            created_user_information.user = created_user

            created_user_information.save()

            if studentinformation_form.faculty and studentinformation_form.s_number:
                created_student_information = studentinformation_form.save(commit=False)

                created_student_information.userinformation = created_user_information

                created_student_information.save()

                mail = created_student_information.s_number + '@mail.zih.tu-dresden.de'

            else:
                mail = created_user.email

            activationMail(created_user, request)
            return render(
                request,
                'registration/success.html',
                {
                    'title': _('Registration successfull'),
                    'acc': mail
                }
            )
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


def activationMail(user, request):
    if settings.DEBUG:
        print('activation email for user {} not sent'.format(user.username))
        user.is_active = True
        user.save()
    else:
        user_token = generateToken()
        Activation.objects.create(user=user, token=user_token)
        activateurl = request.build_absolute_uri() + '?token=' + user_token
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
            _('Your registration at the iFSR course enrollment system'),
            message,
            mailsettings.sender,
            [userinf.studentinformation if userinf.is_student() else user.email],
            mailsettings.auth_user,
            mailsettings.auth_pass
        )
        # print(user_token)


@login_required
def verify_student(request):

    if request.method == "POST":
        form = StudentVerificationForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.userinformation = request.user.userinformation
            a.user = request.user
            a.save()
            return redirect(
                'user-profile'
            )
    else:
        form = StudentVerificationForm()

    return render(
        request,
        'registration/student-verification.html',
        {'form': form}
    )
