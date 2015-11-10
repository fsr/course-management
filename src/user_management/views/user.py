from user_management.models import Student
from user_management.forms import ModifyUserForm
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
            for prop in filter(lambda p: p in cleaned and cleaned[p] != '', (
                'first_name',
                'last_name',
                'email'
            )):
                user.__setattr__(prop, cleaned[prop])
            for prop in filter(lambda p: p in cleaned and cleaned[p] != '', (
                'faculty'
            )):
                student.__setattr__(prop, cleaned[prop])
            user.save()
            student.save()
        return redirect('modify-user')
    else:
        form = ModifyUserForm()
        return render_with_default(request, 'user/edit.html', {'form': form})


@login_required()
def profile(request):
    return render_with_default(request, 'user/profile.html', {})
