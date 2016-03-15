# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-14 17:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataimport', '0006_auto_20160314_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicatorfield',
            name='data_type',
            field=models.CharField(blank=True, choices=[('NUMERIC', 'numeric'), ('PERCENT', 'percent'), ('STRING', 'string')], help_text='(required)', max_length=30, null=True),
        ),
    ]
