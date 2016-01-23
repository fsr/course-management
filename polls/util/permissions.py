import functools

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from guardian.models import UserObjectPermission

from polls.models import Poll
from util.error.reporting import db_error


def must_be_owner(func):
    """
    The decorated function must take at least 2 parameters, the request, and the name of a poll

    If the current user is the poll owner the decorated function is executed, else
     the user is redirected to the login page

    :param func:
    :return:
    """
    @functools.wraps(func)
    @login_required()
    def wrapped(request, poll_name, *args, **kwargs):
        try:
            cur_poll = Poll.objects.get(url=poll_name)
        except Poll.DoesNotExist:
            return db_error(_('This poll does not seem to exist, sorry.'))
        if cur_poll.is_owner(request.user.userinformation):
            return func(request, poll_name, *args, **kwargs)
        else:
            return redirect(reverse('login')+'?next='+request.path)
    return wrapped
