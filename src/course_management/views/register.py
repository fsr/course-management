from course_management.views.base import render_with_default
from course_management.forms import RegistrationForm
from course_management.models.student import Student
from course_management.models.activation import Activation
from django.shortcuts import redirect
import random
import string


def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            userdata = form.cleaned_data
            createduser = Student.create(email=userdata['s_number'] + '@mail.zih.tu-dresden.de',
                                         password=userdata['password'],
                                         first_name=userdata['first_name'],
                                         last_name=userdata['family_name'],
                                         s_number=userdata['s_number'],
                                         faculty=userdata['faculty'])
            if createduser is None:
                return render_with_default(
                    request,
                    'register.html',
                    {'title': 'Registration | iFSR Course Management',
                     'error': 'The s-Number you entered is already in use!',
                     'form': form})
            else:
                activationMail(createduser.user)
                return render_with_default(
                    request,
                    'registration/registrationsuccess.html',
                    {'title': 'Registration successfull | iFSR Course Management',
                     'acc': userdata['s_number']})
        else:
            return render_with_default(
                request,
                'register.html',
                {'title': 'Registration | iFSR Course Management',
                 'error': 'Please check your input.',
                 'form': form})
    else:
        form = RegistrationForm()
        return render_with_default(request, 'register.html', {'title': 'Registration | iFSR Course Management',
                                                              'form': form})


def generateToken(size=50, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def activationMail(user):
    user_token = generateToken()
    newActivation = Activation(user=user, token=user_token)
    newActivation.save()
    print(user_token)
