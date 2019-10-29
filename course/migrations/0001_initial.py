# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('user', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('active', models.BooleanField(default=False)),
                ('max_participants', models.IntegerField()),
                ('description', models.TextField(default='', blank=True)),
                ('archiving', models.CharField(max_length=1, choices=[('t', 'auto'), ('n', 'never'), ('a', 'archived')])),
                ('student_only', models.BooleanField(default=False)),
                ('start_time', models.DateField(default=datetime.date(2016, 1, 24))),
                ('end_time', models.DateField(default=datetime.date(2016, 1, 24))),
                ('participants', models.ManyToManyField(to='user.UserInformation')),
                ('queue', models.ManyToManyField(related_name='waiting_for', to='user.UserInformation')),
            ],
        ),
        migrations.CreateModel(
            name='DateSlot',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('date', models.DateTimeField()),
                ('location', models.CharField(max_length=100, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('subject', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('user', models.ManyToManyField(to='user.UserInformation')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('_type', models.CharField(max_length=1, choices=[('W', 'weekly'), ('O', 'one time')])),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(default='', blank=True)),
                ('description_en', models.TextField(null=True, default='', blank=True)),
                ('description_de', models.TextField(null=True, default='', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='WeeklySlot',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('weekday', models.CharField(max_length=3, choices=[('MON', 'Mondays'), ('TUE', 'Tuesdays'), ('WED', 'Wednesdays'), ('THU', 'Thursdays'), ('FRI', 'Fridays'), ('SAT', 'Saturdays'), ('SUN', 'Sundays')])),
                ('timeslot', models.CharField(max_length=3, choices=[('I', '1st'), ('II', '2nd'), ('III', '3rd'), ('IV', '4th'), ('V', '5th'), ('VI', '6th'), ('VII', '7th')])),
                ('location', models.CharField(max_length=100, blank=True)),
                ('schedule', models.ForeignKey(to='course.Schedule', on_delete=models.deletion.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='dateslot',
            name='schedule',
            field=models.ForeignKey(to='course.Schedule', on_delete=models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='course',
            name='schedule',
            field=models.OneToOneField(to='course.Schedule', on_delete=models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(to='course.Subject', on_delete=models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ManyToManyField(related_name='teacher', to='user.UserInformation'),
        ),
    ]
