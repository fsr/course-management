from django.db import models


class Description(models.Model):
    name = models.CharField(max_length=180, unique=True)
    desc = models.TextField()
