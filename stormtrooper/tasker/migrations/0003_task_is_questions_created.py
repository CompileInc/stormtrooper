# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasker', '0002_auto_20160526_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='is_questions_created',
            field=models.BooleanField(default=False),
        ),
    ]
