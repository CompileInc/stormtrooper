# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='csv',
            field=models.FileField(upload_to='tasks/%Y/%m/%d/'),
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set([('question', 'answered_by')]),
        ),
    ]
