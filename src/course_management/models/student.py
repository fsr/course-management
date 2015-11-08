from django.db import models
from django.contrib.auth.models import User
from course_management.models.faculty import Faculty
from . import faculty


class Student(models.Model):
    user = models.OneToOneField(User)
    s_number = models.CharField(max_length=50)
    faculty = models.ForeignKey(faculty.Faculty)

    def __str__(self):
        return '{first} {last}'.format(first=self.user.first_name, last=self.user.last_name)

    @classmethod
    def create(cls, email, password, first_name, last_name, s_number):
        user = User.objects.create_user(
            username=s_number,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name)
        newstudent = Student(
            user=user,
            s_number=s_number,
            faculty=Faculty.objects.get(name="Fakultät Informatik"))
        newstudent.save()
