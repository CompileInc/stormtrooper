# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', jsonfield.fields.JSONField()),
                ('answered_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', jsonfield.fields.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('csv', models.FileField(upload_to='tasks')),
                ('answer_label', models.CharField(default='Answer', max_length=30)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_closed', models.BooleanField(default=False)),
                ('closed_on', models.DateTimeField(null=True, blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='task',
            field=models.ForeignKey(to='tasker.Task'),
        ),
        migrations.AddField(
            model_name='choice',
            name='task',
            field=models.ForeignKey(to='tasker.Task'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='tasker.Question'),
        ),
    ]
