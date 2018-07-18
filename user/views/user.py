from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _

from user.forms import UserForm, UserInformationForm, UserEditForm, PrivacyAgreementForm
from user.models import Faculty

from util.error.reporting import db_error


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

    if user_id is None:
        if request.user.is_authenticated():
            user = request.user

            # require consenting to privacy policy
            if not user.userinformation.accepted_privacy_policy:
                return redirect('privacy-policy-updated')

            template = 'user/profile.html'
            is_own = True
            teacher = user.userinformation.teacher.filter(archiving='t')
            attend = user.userinformation.course_set.filter(archiving='t')
        else:
            return redirect('login')
    else:
        try:
            user = User.objects.get(id=user_id)
            is_own = request.user.id == user.id
        except User.DoesNotExist:
            return db_error(_('This user does not exist'))

        template = 'user/public-profile.html'

    return render(
        request,
        template,
        {
            'course_list_show_subject': True,
            'profiled_user': user,
            'is_own': is_own,
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
