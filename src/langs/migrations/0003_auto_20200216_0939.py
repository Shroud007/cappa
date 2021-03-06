# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-02-16 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('langs', '0002_auto_20200216_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lang',
            name='name',
            field=models.CharField(default=1, max_length=255, verbose_name='имя'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lang',
            name='provider_name',
            field=models.CharField(choices=[('python', 'python'), ('cpp', 'cpp'), ('csharp', 'csharp')], default=1, max_length=255, unique=True, verbose_name='провайдер'),
            preserve_default=False,
        ),
    ]
