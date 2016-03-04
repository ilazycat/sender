# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-01 16:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grade', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='kuaidiInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('belongs_id', models.IntegerField()),
                ('num', models.CharField(max_length=255)),
                ('company', models.CharField(max_length=255)),
                ('updateTime', models.CharField(max_length=255, null=True)),
                ('time', models.CharField(max_length=255, null=True)),
                ('context', models.TextField(null=True)),
            ],
            options={
                'ordering': ['belongs_id'],
            },
        ),
    ]
