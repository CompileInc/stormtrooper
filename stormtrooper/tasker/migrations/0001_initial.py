# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-16 08:07
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', django.contrib.postgres.fields.jsonb.JSONField(default={'choice_id': None, 'verbose': 'Default Answer'})),
                ('answered_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Export',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('export_file', models.FileField(blank=True, null=True, upload_to='exports/%Y/%m/%d/')),
                ('status', models.CharField(choices=[('PS', 'Processing'), ('FR', 'Failure'), ('SS', 'Success')], default='PS', max_length=2)),
                ('created_on', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', django.contrib.postgres.fields.jsonb.JSONField(default={'key1': 'value1', 'key2': 'value2'})),
                ('slug', models.SlugField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('csv', models.FileField(upload_to='tasks/%Y/%m/%d/')),
                ('answer_label', models.CharField(default='Answer', max_length=30)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_closed', models.BooleanField(default=False)),
                ('is_questions_created', models.BooleanField(default=False)),
                ('is_best_of', models.BooleanField(default=False, help_text='Check this if you want to run best-of-n. Default: max-of-n')),
                ('answer_plugin', models.CharField(blank=True, max_length=5, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasker.Task'),
        ),
        migrations.AddField(
            model_name='export',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasker.Task'),
        ),
        migrations.AddField(
            model_name='export',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='choice',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasker.Task'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasker.Question'),
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set([('question', 'answered_by')]),
        ),
    ]
