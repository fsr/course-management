from user.models import Activation
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from user.render_tools import adaptive_render


@adaptive_render
def activate(request, render):
    if request.method == 'GET':
        reqdict = request.GET.dict()
        if 'token' not in reqdict:
            return render(
                request,
                'user/activate.html',
                {'title': 'Activation Failed',
                 'error': 'You didn\'t provide a token.'})
        else:
            try:
                db_entry = Activation.objects.get(token=reqdict['token'])
            except Activation.DoesNotExist:
                return render(
                    request,
                    'user/activate.html',
                    {'title': 'Activation Failed',
                     'error': 'The token you provided is invalid.'})
            db_entry.user.is_active = True
            db_entry.user.save()
            db_entry.delete()
            return render(
                request,
                'user/activate.html',
                {'title': 'Activation Succeded'})
    else:
        return redirect('index')
