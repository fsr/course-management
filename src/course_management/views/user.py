from course_management.models.student import Student
from course_management.forms import ModifyUserForm
from django.contrib.auth.decorators import login_required
from course_management.views.base import render_with_default


@login_required()
def modify(request):

    if request.method == "POST":
        form = ModifyUserForm(request.POST)
        user = request.user
        student = user.student
        if form.is_valid():
            for prop in (
                'first_name',
                'last_name',
                'email',
                'password'
            ):
                if prop in form:
                    user.__setattr__(prop, form[prop])
            for prop in (
                'faculty'
            ):
                if prop in form:
                    student.__setattr__(prop, form[prop])
            user.save()
            student.save()
        return redirect('modify-user')
    else:
        form = ModifyUserForm()
        return render_with_default(request, 'modify-user.html', {'form': form})
