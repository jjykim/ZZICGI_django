# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-17 07:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_profile_filter'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='filter',
            new_name='filters',
        ),
    ]