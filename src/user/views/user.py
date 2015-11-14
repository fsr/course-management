from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from user.forms import ModifyUserForm
from user.models import Faculty
from user.render_tools import adaptive_render
from util.error.reporting import db_error


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

            try:
                student.faculty = Faculty.objects.get(id=int(cleaned['faculty']))
            except Faculty.DoesNotExist:
                return db_error(
                    'Oops, it seems that faculty does not exist. Please try again and should the problem persist '
                    'contact an administrator.'
                )

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
    user = request.user
    return render(request, 'user/profile.html', {
        'course_list': user.student.course_set.all(),
        'course_list_show_subject': True,
    })
