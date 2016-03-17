# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-17 15:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataimport', '0008_auto_20160317_1519'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='lookuptableelement',
            name='system_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataimport.SystemCode'),
        ),
    ]
