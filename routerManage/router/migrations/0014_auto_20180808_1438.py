# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-08-08 06:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('router', '0013_time_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='time',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 8, 14, 38, 22, 624205)),
        ),
    ]
