from course.models import news
from django.shortcuts import render
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
        'privacy.html',
        {
            'title': _('Privacy Policy')
        }
    )
