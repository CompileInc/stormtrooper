# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-23 06:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tasker', '0007_task_is_multiple_choice'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
