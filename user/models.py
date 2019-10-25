from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from markdown import markdown
from django.views.decorators.debug import sensitive_variables

from util.html_clean import clean_for_user_description


def privacy_policy_consented(consented):
    if consented and type(consented) is bool:
        return
    raise ValidationError(
        _('You must agree to the privacy policy to use our services.'))


class Faculty(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class UserInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(default="")
    public_profile = models.BooleanField(default=False)
    accepted_privacy_policy = models.BooleanField(
        validators=[privacy_policy_consented])

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
                return UserInformation.objects.create(user=user, accepted_privacy_policy=True)
            else:
                raise TypeError('I got a faculty but no s number?')
        else:
            if faculty is None or faculty == '':
                raise TypeError('I got an s number but no faculty?')
            else:
                return StudentInformation.objects.create(
                    user=user,
                    accepted_privacy_policy=True,
                    s_number=s_number,
                    faculty=Faculty.objects.get(pk=faculty)
                )

    def is_student(self):
        try:
            self.studentinformation
            return True
        except StudentInformation.DoesNotExist:
            return False

    def is_verified_student(self):
        return self.is_student() and self.studentinformation.verified

    def is_pending_student(self):
        return self.is_student() and not self.studentinformation.verified


class StudentInformation(UserInformation):
    s_number = models.CharField(max_length=50, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT)
    verified = models.BooleanField(default=False)

    def make_zih_mail(self):
        return self.s_number + '@mail.zih.tu-dresden.de'


ACTIVATION_TYPES = {
    'student': 's',
    'email': 'e'
}


class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=50)
    type = models.CharField(max_length=1,
                            choices=tuple((v, k)
                                          for k, v in ACTIVATION_TYPES.items())
                            )


def get_user_information(obj):
    if isinstance(obj, User):
        return obj.userinformation
    elif isinstance(obj, StudentInformation):
        return obj.user.userinformation  # TODO: Ok this way?
    elif isinstance(obj, UserInformation):
        return obj
    elif isinstance(obj, (int, str)):
        return UserInformation.objects.get(id=obj)
    else:
        raise TypeError('Cannot convert {} to {}'.format(
            type(obj, UserInformation)))
