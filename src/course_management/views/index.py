import course_management.views.base

def index(request):
    return render_with_default(request, 'index.html', {})
