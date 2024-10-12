from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from markdown import markdown
from django.views.decorators.debug import sensitive_variables

from util.html_clean import clean_for_user_description


def privacy_policy_consented(consented):
    if consented and type(consented) is bool:
        return
    raise ValidationError(
        _('You must agree to the privacy policy to use our services.'))


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

        return UserInformation.objects.create(user=user, accepted_privacy_policy=True)


ACTIVATION_TYPES = {
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
    elif isinstance(obj, UserInformation):
        return obj
    elif isinstance(obj, (int, str)):
        return UserInformation.objects.get(id=obj)
    else:
        raise TypeError('Cannot convert {} to {}'.format(
            type(obj, UserInformation)))
