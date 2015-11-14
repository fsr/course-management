from course.views.base import render_with_default
from course.models import subject


def index(request):
    return render_with_default(
        request,
        'index.html',
        {
            'title': 'Welcome',
            'subjects': subject.Subject.get_active()
        }
    )
