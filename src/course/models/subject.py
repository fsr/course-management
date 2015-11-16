from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default="")

    def __str__(self):
        return self.name

    @classmethod
    def get_active(cls):
        return cls.objects.annotate(
            course_count=models.Count(models.Q(course__active=True))
        ).filter(course_count__gt=0)

    @property
    def active_courses(self):
        return self.course_set.filter(active=True)
