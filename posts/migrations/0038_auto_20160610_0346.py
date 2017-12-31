# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-09 18:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0037_auto_20160601_0048'),
    ]

    operations = [
        migrations.AddField(
            model_name='secretstorekey',
            name='domination_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='secret_key',
            field=models.ForeignKey(default=-99, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.SecretStoreKey'),
        ),
    ]
