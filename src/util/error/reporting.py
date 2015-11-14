from django.shortcuts import render


def db_error(message):
    return render('error/db.html', {'error': message})
