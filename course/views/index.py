from course.models import subject
from django.shortcuts import render
from django.utils.translation import ugettext as _


def index(request):
    return render(
        request,
        'index.html',
        {
            'title': _('Welcome'),
            'news': news.News.objects.order_by('-id')[:3],
            'subjects': subject.Subject.get_active()
        }
    )
