from django.db import models


class Description(models.Model):
    name = models.CharField(unique=True)
    desc = models.TextField()