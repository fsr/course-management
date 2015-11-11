from user_management.models import Student
from user_management.forms import ModifyUserForm
from django.contrib.auth.decorators import login_required
from course_management.views.base import render_with_default
from django.shortcuts import redirect


@login_required()
def modify(request):
    user = request.user
    student = user.student
    if request.method == "POST":
        form = ModifyUserForm(request.POST)
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