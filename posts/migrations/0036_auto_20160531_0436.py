# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-30 19:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0035_auto_20160524_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'food'), (1, 'hotel')], default=0)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
            ],
        ),
        migrations.RemoveField(
            model_name='photo',
            name='contents',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='title',
        ),
        migrations.AddField(
            model_name='photo',
            name='like',
            field=models.IntegerField(choices=[(0, 'good'), (1, 'bad')], default=0),
        ),
        migrations.AddField(
            model_name='photo',
            name='review',
            field=models.TextField(default='none', verbose_name='review'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='secret_key',
            field=models.ForeignKey(default=-99, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.SecretStoreKey'),
        ),
        migrations.AddField(
            model_name='photo',
            name='survey_check',
            field=models.ManyToManyField(to='posts.Survey'),
        ),
    ]
