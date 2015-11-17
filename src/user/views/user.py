from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect

from user.forms import ModifyUserForm
from user.models import Faculty
from util.render_tools import adaptive_render
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

            student.public_profile = cleaned['public_profile']
            student.description = cleaned['description']

            user.save()
            student.save()

            return redirect('user-profile')

    else:

        form = ModifyUserForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'faculty': student.faculty.id,
            'public_profile': student.public_profile,
            'description': student.description
        })
    return render(
        request,
        'user/edit.html',
        {
            'title': '{} {}'.format(user.first_name, user.last_name),
            'form': form
        }
    )


@adaptive_render
def profile(request, user_id=None, render=None):

    if user_id is None:
        if request.user.is_authenticated():
            user = request.user
            template = 'user/profile.html'
        else:
            return redirect('login')
    else:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return db_error('This user does not exist')

        template = 'user/public-profile.html'

    return render(
        request,
        template,
        {
            'course_list_show_subject': True,
            'profiled_user': user,
            'title': '{} {}'.format(user.first_name, user.last_name)
        }
    )
