from django.db import models
from markdown import markdown
from util.html_clean import clean_for_description

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name

    def render_description(self):
        return clean_for_description(markdown(self.description))

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

    @classmethod
    def get_visible(cls):
        """
        Return al subjects which have associated visible courses.
        """
        return filter(
            lambda subject:subject.is_visible(),
            cls.objects.all()
        )

    @classmethod
    def get_inactive(cls):
        """
        Return all subjects which do not have associated active courses.
        """
        return filter(
            lambda subject: not subject.is_active(),
            cls.objects.all()
        )

    @classmethod
    def get_invisible(cls):
        """
        Return all subjects which do not have associated visible courses.
        """
        return filter(
            lambda subject: not subject.is_visible(),
            cls.objects.all()
        )

    @property
    def active_courses(self):
        """
        Returns all associated courses which are active.
        """
        return self.course_set.filter(active=True, archiving='t')

    def visible_courses(self):
        """
        Returns all associated courses which are visible.
        """
        return self.course_set.filter(visible=True, archiving='t')

    def is_active(self):
        """
        Return true if this subject has any associated courses which are active.
        """
        return self.course_set.filter(active=True, archiving='t').exists()

    def is_visible(self):
        """
        Return true if this subject has any associated courses which are visible.
        """
        return self.course_set.filter(visible=True, archiving='t').exists()
