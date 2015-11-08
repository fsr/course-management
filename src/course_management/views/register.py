from course_management.views.base import render_with_default
from course_management.forms import RegistrationForm
from course_management.models.student import Student
from django.http import HttpResponseRedirect


def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            userdata = form.cleaned_data
            createduser = Student.create(email=userdata['email'],
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
                     'error': 'The s number you entered is already in use!',
                     'form': form})
            else:
                return HttpResponseRedirect('/register/')
        else:
            return render_with_default(
                request,
                'register.html',
                {'title': 'Registration failed | iFSR Course Management',
                 'error': 'Your input was not correct.',
                 'form': form})
    else:
        form = RegistrationForm()
        return render_with_default(request, 'register.html', {'title': 'Registration | iFSR Course Management',
                                                              'form': form})
