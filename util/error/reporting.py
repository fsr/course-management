from django.shortcuts import render


def db_error(request, message):
    """
    Report a database error in a view.
    """
    return render(request, 'error/db.html', {'error': message})
