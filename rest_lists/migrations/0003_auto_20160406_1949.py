# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-06 11:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_lists', '0002_auto_20160406_1746'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='stdUser',
            new_name='UserProfile',
        ),
        migrations.RemoveField(
            model_name='list',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
