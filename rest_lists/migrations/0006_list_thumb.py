# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-07 11:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_lists', '0005_userprofile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='thumb',
            field=models.ImageField(blank=True, default='/img/default.svg', upload_to='rest_pics'),
        ),
    ]
