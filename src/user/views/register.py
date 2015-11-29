import random
import string

from django.core.mail import send_mail
from django.shortcuts import render
from django.conf import settings
from django.utils.translation import ugettext as _

from user import mailsettings
from user.forms import RegistrationForm
from user.models import UserInformation, Activation

from re_captcha.decorators import re_captcha_verify


@re_captcha_verify
def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            userdata = form.cleaned_data
            createduser = UserInformation.create(
                username=userdata['username'],
                email=userdata['email'],
                password=userdata['password'],
                first_name=userdata['first_name'],
                last_name=userdata['family_name'],
                s_number=userdata.get('s_number', None),
                faculty=userdata.get('faculty', None)
            )
            activationMail(createduser.user, request)
            return render(
                request,
                'registration/success.html',
                {
                    'title': _('Registration successfull'),
                    'acc': createduser.studentinformation.s_number + '@mail.zih.tu-dresden.de'
                    if createduser.is_student() else createduser.email
                }
            )
    else:
        form = RegistrationForm()

    return render(
        request,
        'registration/register.html',
        {
            'title': _('Registration'),
            'form': form
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
