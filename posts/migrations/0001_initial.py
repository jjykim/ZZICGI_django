# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-16 20:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'location'), (1, 'tag')], default=0, max_length=1)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.URLField(default='/url')),
                ('sns_type', models.IntegerField(choices=[(0, 'facebook'), (1, 'kakaotalk')], default=0, max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='title')),
                ('location', models.CharField(max_length=500, verbose_name='location')),
            ],
        ),
        migrations.AddField(
            model_name='photo',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Store'),
        ),
        migrations.AddField(
            model_name='filter',
            name='store',
            field=models.ManyToManyField(to='posts.Store'),
        ),
    ]
