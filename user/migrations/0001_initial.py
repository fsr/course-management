# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('token', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=1, choices=[('s', 'student'), ('e', 'email')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('description', models.TextField(default='')),
                ('public_profile', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='StudentInformation',
            fields=[
                ('userinformation_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, parent_link=True, to='user.UserInformation', on_delete=models.deletion.CASCADE)),
                ('s_number', models.CharField(max_length=50, unique=True)),
                ('verified', models.BooleanField(default=False)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.Faculty')),
            ],
            bases=('user.userinformation',),
        ),
        migrations.AddField(
            model_name='userinformation',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.deletion.CASCADE),
        ),
    ]
