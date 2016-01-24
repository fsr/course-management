# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import polls.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('value', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ChoiceCounter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('counter', models.BigIntegerField(default=0)),
                ('choice', models.ForeignKey(related_name='counters', to='polls.Choice')),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('url', models.CharField(unique=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='QLink',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('required', models.BooleanField(default=True)),
                ('position', models.IntegerField(default=polls.models.qlink_next_position)),
                ('poll', models.ForeignKey(related_name='questions', to='polls.Poll')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('question', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='QValue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('value', models.CharField(max_length=500)),
                ('question', models.ForeignKey(related_name='fulltext_answers', to='polls.QLink')),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('token', models.CharField(max_length=20)),
                ('used', models.BooleanField(default=False)),
                ('poll', models.ForeignKey(related_name='tokens', to='polls.Poll')),
            ],
        ),
        migrations.AddField(
            model_name='qlink',
            name='question',
            field=models.ForeignKey(related_name='values', to='polls.Question'),
        ),
        migrations.AddField(
            model_name='choicecounter',
            name='qlink',
            field=models.ForeignKey(related_name='counters', to='polls.QLink'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(related_name='choices', to='polls.Question'),
        ),
    ]
