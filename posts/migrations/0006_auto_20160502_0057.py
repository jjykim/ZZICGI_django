# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 15:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_store_location'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='filter',
            new_name='filters',
        ),
    ]