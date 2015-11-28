from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import render, redirect

from user.forms import ContactForm
from util.error.reporting import db_error


@login_required
def contact_form(request:HttpRequest, user_id:int):

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return db_error('User does not exist')
    assert isinstance(user, User)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            user.email_user(
                subject="[CM contact form] " + form.subject,
                message=form.content,
                from_email=form.sender
            )
            return redirect('index')
    else:
        form = ContactForm()

    return render(
        request,
        'contact-form.html',
        {'form': form, 'user_id': user_id}
    )
