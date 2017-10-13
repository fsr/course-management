from django.db import models

from guardian.models import UserObjectPermission
from user.models import UserInformation, get_user_information
from util.html_clean import clean_for_description

class News(models.Model):
    headline = models.CharField(max_length=30)
    entry = models.TextField(blank=True, default="")

    def __str__(self):
        return self.headline

    def edit_news(self, headl, entry):
        self.headl.add(headl)
        self.entry.add(entry)
