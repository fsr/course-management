# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='end_time',
            field=models.DateField(default=datetime.date(2016, 4, 6)),
        ),
        migrations.AlterField(
            model_name='course',
            name='start_time',
            field=models.DateField(default=datetime.date(2016, 4, 6)),
        ),
    ]
