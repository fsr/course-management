from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError
from markdown import markdown

from util.html_clean import clean_for_user_description


class Faculty(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User)
    s_number = models.CharField(max_length=50)
    faculty = models.ForeignKey(Faculty)
    public_profile = models.BooleanField(default=False)
    description = models.TextField(default="")

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

    def render_description(self):
        return clean_for_user_description(markdown(self.description))


class Activation(models.Model):
    user = models.OneToOneField(User)
    token = models.CharField(max_length=50)
