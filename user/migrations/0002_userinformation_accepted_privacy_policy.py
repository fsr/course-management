# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinformation',
            name='accepted_privacy_policy',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
