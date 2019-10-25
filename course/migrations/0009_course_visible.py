# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='visible',
            field=models.BooleanField(default=False),
        ),
    ]
