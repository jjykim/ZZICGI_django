# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-09 19:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0039_auto_20160610_0417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='secret_key',
            field=models.ForeignKey(default=-99, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.SecretStoreKey'),
        ),
        migrations.AlterField(
            model_name='secretstorekey',
            name='domination_date',
            field=models.DateField(null=True),
        ),
    ]