from django.db import models

class News(models.Model):
    headline = models.CharField(max_length=30)
    entry = models.TextField(blank=True, default="")

    def __str__(self):
        return self.headline