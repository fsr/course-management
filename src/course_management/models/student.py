from django.db import models
from django.contrib.auth.models import User
from course_management.models.faculty import Faculty
from . import faculty
from django.db import IntegrityError


class Student(models.Model):
    user = models.OneToOneField(User)
    s_number = models.CharField(max_length=50)
    faculty = models.ForeignKey(faculty.Faculty)

    def __str__(self):
        return '{first} {last}'.format(first=self.user.first_name, last=self.user.last_name)

    @classmethod
    def create(cls, email, password, first_name, last_name, s_number, faculty):
        '''
        This function creates a new user/student and saves it to the database.
        When using this function, the created user will be set 'inactive'
        by default.
        '''
        try:
            user = User.objects.create_user(
                username=s_number,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name)
            # set user inactive
            user.is_active = False
            user.save()
            newstudent = Student(
                user=user,
                s_number=s_number,
                faculty=Faculty.objects.get(pk=faculty))
            newstudent.save()
            return newstudent
        except IntegrityError:
            return None
