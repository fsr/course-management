from course_management.views.base import render_with_default
from course_management.forms import RegistrationForm
from course_management.models.student import Student
from course_management.models.faculty import Faculty
from django.contrib.auth.models import User


def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            userdata = form.cleaned_data
            user = User.objects.create_user(userdata['s_number'], userdata['email'], userdata['password'])
            newstudent = Student(user=user, s_number=userdata['s_number'], faculty=Faculty.objects.get(name="Fakultät Informatik"))
            newstudent.save()
            print("YES")

        else:
            print("NO")
    else:
        form = RegistrationForm()
        return render_with_default(request, 'register.html', {'title': 'Registration | iFSR Course Management',
                                                              'form': form})
