from course_management.views.base import render_with_default
from course_management.forms import RegistrationForm



def register(request):

    if request.method == 'POST':
        # print(request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print("YES")
        else:
            print("NO")
    else:
        form = RegistrationForm()
        return render_with_default(request, 'register.html', {'title': 'Registration | iFSR Course Management',
                                                              'form': form})
