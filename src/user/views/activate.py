from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_GET

from user.models import Activation

from util.render_tools import adaptive_render


@adaptive_render
@require_GET
def activate(request, render):

    def activation_error(error):
        return render(
            request,
            'user/activate.html',
            {
                'title': 'Activation Failed',
                'error': error
            }
        )

    reqdict = request.GET
    if 'token' not in reqdict:
        return activation_error('You didn\'t provide a token.')
    else:
        try:
            db_entry = Activation.objects.get(token=reqdict['token'])
        except Activation.DoesNotExist:
            return activation_error('The token you provided is invalid.')
        db_entry.user.is_active = True
        db_entry.user.save()
        db_entry.delete()
        return render(
            request,
            'user/activate.html',
            {'title': 'Activation Succeded'})
