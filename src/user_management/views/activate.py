from course_management.views.base import render_with_default
from user_management.models import Activation
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist


def activate(request):
    if request.method == 'GET':
        reqdict = request.GET.dict()
        if 'token' not in reqdict:
            return render_with_default(
                request,
                'user/activate.html',
                {'title': 'Failure | iFSR Course Management',
                 'error': 'You didn\'t provide a token.'})
        else:
            try:
                db_entry = Activation.objects.get(token=reqdict['token'])
            except ObjectDoesNotExist:
                return render_with_default(
                    request,
                    'user/activate.html',
                    {'title': 'Failure | iFSR Course Management',
                     'error': 'The token you provided is invalid.'})
            db_entry.user.is_active = True
            db_entry.user.save()
            db_entry.delete()
            return render_with_default(
                request,
                'user/activate.html',
                {'title': 'Success | iFSR Course Management'})
    else:
        return redirect('index')
