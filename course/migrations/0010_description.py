# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-10-25 17:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0009_course_visible'),
    ]

    operations = [
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length='180', unique=True)),
                ('desc', models.TextField()),
            ],
        ),
    ]
