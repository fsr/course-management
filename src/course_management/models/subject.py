from django.db import models
from django.db.models import Count


class Subject(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(default="")

    def __str__(self):
        return self.name

    @classmethod
    def get_active(cls):
        return cls.objects.annotate(course_count=Count('course')).filter(course_count__gt=0)
