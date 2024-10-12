from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

from user.models import Activation, ACTIVATION_TYPES
from user.views.register import verification_mail


VERIFICATIONS = {}
# TODO: This is so over-engineered


class RegisterVerification:
    def __init__(self, name, action, view=None):
        if name not in VERIFICATIONS:
            VERIFICATIONS[name] = self

        self.action = action
        if view:
            self.view = view
        else:
            self.view = no_verify_view
        self.name = name


def no_verify_view(request):
    return render(
        request,
        'view-error.html',
        { 'message': _('This verification does not have an associated view.') }
    )


def verify(request, type_):

    if 'token' not in request.GET or type_.lower() not in VERIFICATIONS:
        try:
            return VERIFICATIONS[type_.lower()].view(request)
        except KeyError:
            return render(
                request,
                'view-error.html',
                { 'message': _('This verification does not exist') }
            )
    else:
        try:
            db_entry = Activation.objects.get(token=request.GET['token'], type=ACTIVATION_TYPES[type_])
        except Activation.DoesNotExist:
            return render(
                request,
                'view-error.html',
                { 'message': _('The token you provided is invalid.') }
            )

        VERIFICATIONS[type_.lower()].action(db_entry.user)
        db_entry.delete()
        return render(
            request,
            'user/activate.html',
            {
                'title': _('Activation Succeded'),
                'no_login_redirect': True,
            }
        )


def verify_user(user):
    user.is_active = True
    user.save()


RegisterVerification(action=verify_user, name='email')
