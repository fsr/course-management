from django.http import HttpRequest
from django.shortcuts import redirect


def redirect_unless_target(request: HttpRequest, *args, _target_kwd='target', **kwargs):
    """
    Redirects with 'target' get request parameter awareness.
    """
    return redirect(request.GET[_target_kwd]) if _target_kwd in request.GET else redirect(*args, **kwargs)
