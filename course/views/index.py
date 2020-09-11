from course.models import news
from django.shortcuts import render, render_to_response
from django.utils.translation import ugettext as _


def index(request):
    return render(
        request,
        'new_ui_foo/index.html',
        {
            'title': _('Welcome'),
            'news': news.News.objects.order_by('-id')
        }
    )


def privacy_policy(request):
    return render(
        request,
        'new_ui_foo/privacy.html',
        {
            'title': _('Privacy Policy')
        }
    )


def handler404(request, exception, template_name="new_ui_foo/error/404.html"):
    response = render_to_response(template_name)
    response.status_code = 404
    return response


def handler500(request): #t, exception, template_name="new_ui_foo/error/500.html"):
    template_name = "new_ui_foo/error/500.html"
    response = render_to_response(template_name)
    response.status_code = 500
    return response
