from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOne(User)
    s_nummer = 
