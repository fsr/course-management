from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _

from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

from user.models import Activation, ACTIVATION_TYPES
from user.forms import StudentVerificationForm
from user.views.register import verification_mail


VERIFICATIONS = {}


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

    if 'token' not in request.GET:
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


def verify_student(user):
    user.is_active = True
    user.save()
    si = user.userinformation.studentinformation
    si.verified = True
    si.save()


@login_required
def verify_student_form(request):
    if request.user.userinformation.is_verified_student():
        return redirect(
            'user-profile'
        )
    if request.method == "POST":
        if request.user.userinformation.is_pending_student():
            form = StudentVerificationForm(request.POST, instance=request.user.userinformation.studentinformation)
        else:
            form = StudentVerificationForm(request.POST)
        if form.is_valid():
            if request.user.userinformation.is_pending_student():
                a = form.save()
            else:
                a = form.save(commit=False)
                a.userinformation_ptr = request.user.userinformation
                a.user = request.user
                a.save()
            zih_mail = a.make_zih_mail()
            verification_mail(a.user, 'student', zih_mail)
            return render(
                request,
                'registration/sent-student-verification-mail.html',
                {
                    'title': _('Verification mail sent'),
                    'acc': zih_mail,
                    'no_login_redirect': True,
                }
            )
    else:
        form = StudentVerificationForm()

    return render(
        request,
        'registration/student-verification.html',
        {
            'form': form,
            'no_login_redirect': True,
        }
    )


RegisterVerification(action=verify_student, name='student', view=verify_student_form)
RegisterVerification(action=verify_user, name='email')
