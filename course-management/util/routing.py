from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import resolve, Resolver404


def redirect_unless_target(request: HttpRequest, *args, _target_kwd='target', **kwargs):
    """
    Redirects with 'target' get request parameter awareness.
    Validates that the target URL is an internal URL to prevent open redirects.
    """
    if _target_kwd in request.GET:
        target_url = request.GET[_target_kwd]
        # Validate that the target is an internal URL (starts with /)
        # This prevents open redirect vulnerabilities
        if target_url.startswith('/'):
            try:
                # Try to resolve the URL to ensure it's a valid internal URL
                resolve(target_url)
                return redirect(target_url)
            except Resolver404:
                # Invalid internal URL, fall through to default redirect
                pass
    return redirect(*args, **kwargs)
