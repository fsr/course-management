from django.db import models
from django.contrib.auth.models import User


class Activation(models.Model):
    user = models.OneToOneField(User)
    token = models.CharField(max_length=50)
