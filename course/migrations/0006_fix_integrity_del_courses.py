# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def flush_tables(apps, schema_editor):
    Courses = apps.get_model("course", "Course")
    Courses.objects.all().delete()
    Schedules = apps.get_model("course", "Schedule")
    Schedules.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_auto_20160622_2313'),
    ]

    operations = [
        migrations.RunPython(flush_tables),
        migrations.RemoveField("Course", "schedule"),
        migrations.AddField(
            model_name="Schedule",
            name="course",
            field=models.OneToOneField("Course")
        )
    ]
