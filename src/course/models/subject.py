from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default="")

    def __str__(self):
        return self.name

    @classmethod
    def get_active(cls):
        """
        Return all subjects which have associated active courses.
        """
        # REVIEW
        # This does not work right now, I have no idea why
        # return cls.objects.annotate(
        #     course_count=models.Count(models.Q(course__active=True))
        # ).filter(course_count__gt=0)
        return filter(
            lambda subject: subject.is_active(),
            cls.objects.all()
        )

    @property
    def active_courses(self):
        """
        Returns all associated courses which are active.
        """
        return self.course_set.filter(active=True)

    def is_active(self):
        """
        Return true if this subject has any associated courses which are active.
        """
        return self.course_set.filter(active=True).exists()
