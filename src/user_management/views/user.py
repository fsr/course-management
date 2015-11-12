from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from course_management.views.base import render_with_default
from user_management.models import Student
from user_management.forms import ModifyUserForm


@login_required()
def modify(request):

    user = request.user
    student = user.student

    if request.method == "POST":

        form = ModifyUserForm(request.POST)

        if form.is_valid():

            cleaned = form.cleaned_data

            # should we verify something here?
            user.first_name = cleaned['first_name']
            user.last_name = cleaned['last_name']
            user.email = cleaned['email']

            student.faculty = cleaned['faculty']

            user.save()
            student.save()

        return redirect('modify-user')

    else:

        form = ModifyUserForm({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'faculty': student.faculty.id
        })
        return render_with_default(request, 'user/edit.html', {'form': form})


@login_required()
def profile(request):
    return render_with_default(request, 'user/profile.html', {})
