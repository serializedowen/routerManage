# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-07-22 05:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('router', '0002_auto_20180722_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ip',
            name='post',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
