from course_management.views.base import render_with_default


def login(request):
    return render_with_default(request, 'login.html', {'title': 'Sign in'})