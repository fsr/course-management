from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext as _

from user.forms import AbstractContactForm
from util.error.reporting import db_error

CONTACT_FOOTER = """
-------------------
This message has been sent via the Course Mangement System.
Sent by: """

@login_required
@csrf_protect
def contact_form(request: HttpRequest, user_id: int):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return db_error(_('Requested user does not exist.'))
    assert isinstance(user, User)

    if request.method == 'POST':
        form = AbstractContactForm(request.POST)
        if form.is_valid():
            content = form.content + CONTACT_FOOTER + request.user.email
            user.email_user(
                subject="[CM contact form] " + form.subject,
                message=content
            )
            return redirect('index')
    else:
        form = AbstractContactForm()

    return render(
        request,
        'new_ui_foo/contact-form.html',
        {
            'form': form,
            'user': user
        }
    )
