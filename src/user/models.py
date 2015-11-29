from markdown import markdown

from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError

from util.html_clean import clean_for_user_description


class Faculty(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class UserInformation(models.Model):
    user = models.OneToOneField(User)
    description = models.TextField(default="")
    public_profile = models.BooleanField(default=False)

    def __str__(self):
        return '{first} {last}'.format(first=self.user.first_name, last=self.user.last_name)

    def render_description(self):
        return clean_for_user_description(markdown(self.description))

    @staticmethod
    def create(
        username,
        email,
        password,
        first_name,
        last_name,
        s_number=None,
        faculty=None
    ):
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_active = False
        user.save()

        if s_number is None or s_number == '':
            if faculty is None or faculty == '':
                return UserInformation.objects.create(user=user)
            else:
                raise TypeError('I got a faculty but no s number?')
        else:
            if faculty is None or faculty == '':
                raise TypeError('I got an s number but no faculty?')
            else:
                return StudentInformation.objects.create(
                    user=user,
                    s_number=s_number,
                    faculty=Faculty.objects.get(pk=faculty)
                )

    def is_student(self):
        try:
            self.studentinformation
            return True
        except StudentInformation.DoesNotExist:
            return False



class StudentInformation(UserInformation):
    s_number = models.CharField(max_length=50, unique=True)
    faculty = models.ForeignKey(Faculty)


class Activation(models.Model):
    user = models.OneToOneField(User)
    token = models.CharField(max_length=50)


def get_user_information(obj):
    if isinstance(obj, (User, StudentInformation)):
        return user.userinformation
    elif isinstance(obj, UserInformation):
        return obj
    elif isinstance(obj, (int, str)):
        return UserInformation.objects.get(id=obj)
    else:
        raise TypeError('Cannot convert {} to {}'.format(type(obj, UserInformation)))
