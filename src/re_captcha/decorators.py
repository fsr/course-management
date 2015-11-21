from functools import wraps
from django.conf import settings
import requests
from django.shortcuts import render


def re_captcha_verify(func):

    if settings.RE_CAPTCHA_VERIFY:

        @wraps(func)
        def wrapper(request, *args, **kwargs):

            if request.method == 'post':

                if 'g-recaptcha-response' in request.POST:
                    r = request.post(
                        'https://www.google.com/recaptcha/api/siteverify',
                        data={
                            'secret': settings.RE_CAPTCHA_SECRET_KEY,
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
