from course.models import news
from django.shortcuts import render
from django.utils.translation import gettext as _


def index(request):
    return render(
        request,
        'index.html',
        {
            'title': _('Welcome'),
            'news': news.News.objects.order_by('-id')
        }
    )


def privacy_policy(request):
    return render(
        request,
        'privacy.html',
        {
            'title': _('Privacy Policy')
        }
    )


def handler404(request, exception, template_name="error/404.html"):
    response = render(request, template_name)
    response.status_code = 404
    return response


def handler500(request): #t, exception, template_name="error/500.html"):
    template_name = "error/500.html"
    response = render(request, template_name)
    response.status_code = 500
    return response
