# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-11 20:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasker', '0008_export'),
    ]

    operations = [
        migrations.AddField(
            model_name='export',
            name='status',
            field=models.CharField(choices=[('PS', 'Processing'), ('FR', 'Failure'), ('SS', 'Success')], default='PS', max_length=2),
        ),
        migrations.AddField(
            model_name='export',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='export',
            name='export_file',
            field=models.FileField(blank=True, null=True, upload_to='exports/%Y/%m/%d/'),
        ),
    ]