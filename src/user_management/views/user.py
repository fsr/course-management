from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from user_management.forms import ModifyUserForm
from user_management.render_tools import adaptive_render


@login_required()
@adaptive_render
def modify(request, render):

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
        return render(request, 'user/edit.html', {'form': form})


@login_required()
@adaptive_render
def profile(request, render):
    return render(request, 'user/profile.html', {})
