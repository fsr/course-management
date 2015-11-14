from django.shortcuts import render_to_response


def db_error(message):
    return render_to_response('error/db.html', {'error': message})
