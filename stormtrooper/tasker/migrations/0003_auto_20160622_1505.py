# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-22 15:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasker', '0002_auto_20160621_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='export',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
