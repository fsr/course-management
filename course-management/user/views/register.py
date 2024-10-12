import random
import string
import os

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.translation import gettext as _
from django.views.decorators.debug import sensitive_post_parameters, sensitive_variables

from user.forms import UserInformationForm, UserForm
from user.models import UserInformation, Activation, ACTIVATION_TYPES


@sensitive_post_parameters('password1', 'password2')
@sensitive_variables('password1', 'password2')
def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        userinformation_form = UserInformationForm(request.POST)
        if (user_form.is_valid()
                and userinformation_form.is_valid()):

            created_user = user_form.save(commit=False)
            created_user.is_active = False
            created_user.save()

            created_user_information = userinformation_form.save(
                commit=False)

            created_user_information.user = created_user

            created_user_information.save()

            verification_mail(created_user, 'email',
                                created_user.email, request)

            acc = created_user.email

            return render(
                request,
                'registration/success.html',
                {
                    'title': _('Registration successfull'),
                    'mail': acc
                }
            )
        else:
            print('validation failed')
    else:
        user_form = UserForm()
        userinformation_form = UserInformationForm()

    return render(
        request,
        'registration/register.html',
        {
            'title': _('Registration'),
            'user_form': user_form,
            'userinformation_form': userinformation_form,
        }
    )


def generateToken(size=50, chars=None):
    chars = (chars
             if chars is not None
             else string.ascii_uppercase + string.digits + string.ascii_lowercase
             )
    return ''.join(random.sample(chars, size))


def verification_mail(user, type_, email, request):
    type_ = type_.lower()
    type_val = ACTIVATION_TYPES[type_]

    user_token = generateToken()

    Activation.objects.create(user=user, token=user_token, type=type_val)
    activateurl = request.build_absolute_uri(
        reverse('verify', args=[type_])) + '?token=' + user_token
    # print(activateurl)
    with open(os.path.join(settings.BASE_DIR, 'res/registrationmail.txt')) as f:
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
        None,
        [email],
    )
    # print(user_token)
