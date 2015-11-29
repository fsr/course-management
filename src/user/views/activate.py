from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _

from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_GET

from user.models import Activation


@require_GET
def activate(request):

    def activation_error(error):
        return render(
            request,
            'user/activate.html',
            {
                'title': _('Activation Failed'),
                'error': error
            }
        )

    reqdict = request.GET
    if 'token' not in reqdict:
        return activation_error(_('You didn\'t provide a token.'))
    else:
        try:
            db_entry = Activation.objects.get(token=reqdict['token'])
        except Activation.DoesNotExist:
            return activation_error(_('The token you provided is invalid.'))
        db_entry.user.is_active = True
        db_entry.user.save()
        db_entry.delete()
        return render(
            request,
            'user/activate.html',
            {'title': _('Activation Succeded')}
        )
