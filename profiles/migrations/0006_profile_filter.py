# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-17 06:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20160417_0611'),
        ('profiles', '0005_profile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='filter',
            field=models.ManyToManyField(to='posts.Filter'),
        ),
    ]