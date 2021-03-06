# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-09 13:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inscription', '0008_auto_20170909_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='identification',
            field=models.CharField(max_length=20, unique=True, verbose_name='Identification'),
        ),
        migrations.AlterUniqueTogether(
            name='inscriptionslot',
            unique_together=set([('inscription', 'slot')]),
        ),
    ]
