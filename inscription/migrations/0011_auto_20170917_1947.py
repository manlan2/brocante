# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-17 19:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inscription', '0010_auto_20170913_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscriptionslot',
            name='slot',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='inscription.Slot', verbose_name='Slot'),
        ),
        migrations.AlterUniqueTogether(
            name='inscriptionslot',
            unique_together=set([]),
        ),
    ]
