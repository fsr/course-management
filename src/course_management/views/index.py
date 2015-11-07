from course_management.views.base import render_with_default

def index(request):
    return render_with_default(request, 'index.html', {})
