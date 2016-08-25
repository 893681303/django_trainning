# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-15 08:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_posts_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='posts',
            name='publish',
            field=models.DateField(default=datetime.datetime(2016, 8, 15, 8, 11, 27, 618586, tzinfo=utc)),
            preserve_default=False,
        ),
    ]