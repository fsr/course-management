from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.debug import sensitive_post_parameters

from user.forms import UserForm, UserInformationForm, UserEditForm, PrivacyAgreementForm

from course.views.index import handler404

from util.error.reporting import db_error


@sensitive_post_parameters('password1', 'password2')
@login_required()
def modify(request):
    user = request.user
    student = user.userinformation

    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=request.user)
        userinformation_form = UserInformationForm(
            request.POST, instance=request.user.userinformation)

        if user_form.is_valid() and userinformation_form.is_valid():
            user.save()
            userinformation_form.save()
            return redirect('user-profile')
    else:
        user_form = UserEditForm(instance=request.user)
        userinformation_form = UserInformationForm(
            instance=request.user.userinformation)

    return render(
        request,
        'user/edit.html',
        {
            'title': '{} {}'.format(user.first_name, user.last_name),
            'user_form': user_form,
            'userinformation_form': userinformation_form
        }
    )


def profile(request, user_id=None):
    attend = []
    if user_id is None:
        if request.user.is_authenticated:
            user = request.user

            # require consenting to privacy policy
            if not user.userinformation.accepted_privacy_policy:
                return redirect('privacy-policy-updated')

            template = 'user/profile.html'

            is_own = True
            # construct a list of attended courses that are not yet archived
            attend = [(p.course, p.course.position_in_queue(user.userinformation)) for p in user.userinformation.participation_set.all() if p.course.archiving == 't']
        else:
            return redirect('login')
    else:
        try:
            user = User.objects.get(id=user_id)
            is_own = request.user.id == user.id
        except User.DoesNotExist:
            return handler404(request, None)

        if not is_own and not (hasattr(user, "userinformation") and user.userinformation.public_profile):
            return handler404(request, None)

        template = 'user/public_profile.html'

    return render(
        request,
        template,
        {
            'course_list_show_subject': True,
            'profiled_user': user,
            'is_own': is_own,
            'attend': attend,
            'title': '{} {}'.format(user.first_name, user.last_name)
        }
    )


@login_required
def privacy_consent(request):
    user = request.user
    user_info = user.userinformation

    # users who have consented already are not in scope for this
    if user_info.accepted_privacy_policy:
        return redirect('user-profile')

    if request.method == "POST":
        # validate the form
        agreement_form = PrivacyAgreementForm(
            request.POST, instance=request.user.userinformation)

        if agreement_form.is_valid():
            user_info.save()
            return redirect('user-profile')
    else:
        agreement_form = PrivacyAgreementForm()

    return render(
        request,
        "user/privacy-agreement.html",
        {
            'title': "Privacy Policy",
            'agreement_form': agreement_form,
        }
    )


@login_required
def delete_account(request):
    if request.method == "POST" and "delete-confirm" in request.POST:
        user = request.user
        user.delete()

        return render(
            None,
            "user/deletion-success.html",
            {
                'title': "Account Deletion Successful"
            }
        )
    else:
        return redirect('modify-user')
