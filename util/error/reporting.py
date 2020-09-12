from django.shortcuts import render_to_response


def db_error(message):
    """
    Report a database error in a view.
    """
    return render_to_response('error/db.html', {'error': message})
