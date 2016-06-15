# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-15 06:43
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasker', '0009_auto_20160611_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={'choice_id': None, 'verbose': 'Default Answer'}),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={'key1': 'value1', 'key2': 'value2'}),
        ),
    ]