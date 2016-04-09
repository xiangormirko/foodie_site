# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-09 07:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rest_lists', '0009_auto_20160409_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posted_time', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('posted_time',),
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='default',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]