# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-04 15:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inscription', '0005_messagehistory_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscription',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email'),
        ),
    ]
