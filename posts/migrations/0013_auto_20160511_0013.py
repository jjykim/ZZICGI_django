# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-10 15:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_auto_20160511_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='secret_key',
            field=models.ForeignKey(default='-99', on_delete=django.db.models.deletion.CASCADE, to='posts.SecretStoreKey'),
        ),
    ]
