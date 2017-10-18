# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_fix_integrity_del_courses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='participants',
            field=models.ManyToManyField(blank=True, to='user.UserInformation'),
        ),
        migrations.AlterField(
            model_name='course',
            name='queue',
            field=models.ManyToManyField(blank=True, related_name='waiting_for', to='user.UserInformation'),
        ),
        migrations.AlterField(
            model_name='course',
            name='teacher',
            field=models.ManyToManyField(blank=True, related_name='teacher', to='user.UserInformation'),
        ),
    ]
