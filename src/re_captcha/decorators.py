from functools import wraps

import requests

from django.conf import settings
from django.shortcuts import render


SECRET = settings.RE_CAPTCHA_SECRET_KEY
VERIFY = getattr(settings, 'RE_CAPTCHA_VERIFY', True)
URL = 'https://www.google.com/recaptcha/api/siteverify'


def re_captcha_verify(func):

    if VERIFY:

        @wraps(func)
        def wrapper(request, *args, **kwargs):

            if request.method == 'post':

                if 'g-recaptcha-response' in request.POST:
                    r = request.post(
                        URL,
                        data={
                            'secret': SECRET_KEY,
                            'response': request.POST['g-recaptcha-response'],
                            'remoteip': request.META['REMOTE_ADDR']
                        }
                    )
                    obj = r.json()
                    if obj['success'] == True:
                        return func(request, *args, **kwargs)

                    elif setting.DEBUG:
                        return captcha_error(obj['error-codes'])


                return captcha_error()
            else:
                return func(request, *args, **kwargs)

        return wrapper

    else:
        return func


def captcha_error(message=''):
    return render_to_reponse('captcha-error.html', {'message':message})
