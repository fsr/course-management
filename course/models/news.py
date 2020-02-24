from django.db import models
from markdown import markdown
from util.html_clean import clean_for_description

class News(models.Model):
    headline = models.CharField(max_length=30)
    entry = models.TextField(blank=True, default="")

    def __str__(self):
        return self.headline

    def render_entry(self):
        return clean_for_description(markdown(self.entry))
