# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20160417_0611'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='location',
        ),
        migrations.AddField(
            model_name='store',
            name='lat',
            field=models.CharField(default='none', max_length=500, verbose_name='lat'),
        ),
        migrations.AddField(
            model_name='store',
            name='lng',
            field=models.CharField(default='none', max_length=500, verbose_name='lng'),
        ),
        migrations.AddField(
            model_name='store',
            name='main',
            field=models.CharField(default='none', max_length=500, verbose_name='main'),
        ),
    ]
