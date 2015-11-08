from course_management.models.student import Student
from course_management.forms import ModifyUserForm
from django.contrib.auth.decorators import login_required
from course_management.views.base import render_with_default
from django.shortcuts import redirect


@login_required()
def modify(request):

    if request.method == "POST":
        form = ModifyUserForm(request.POST)
        user = request.user
        student = user.student
        if form.is_valid():
            cleaned = form.cleaned_data
            print(cleaned)
            for prop in (
                'first_name',
                'last_name',
                'email'
            ):
                if prop in cleaned:
                    print(cleaned[prop])
                    user.__setattr__(prop, cleaned[prop])
            for prop in (
                'faculty'
            ):
                if prop in cleaned:
                    student.__setattr__(prop, cleaned[prop])
            user.save()
            student.save()
        return redirect('modify-user')
    else:
        form = ModifyUserForm()
        return render_with_default(request, 'modify-user.html', {'form': form})
