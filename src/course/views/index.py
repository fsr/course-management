from course.models import subject
from django.shortcuts import render


def index(request):
    return render(
        request,
        'index.html',
        {
            'title': 'Welcome',
            'subjects': subject.Subject.get_active()
        }
    )
