# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-11 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0019_auto_20160310_1912'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='districtindicatordetaildataset',
            name='display_type',
            field=models.CharField(choices=[('BAR-CHART', 'Bar Chart'), ('BASIC-BAR-CHART', 'Bar Chart (Basic)'), ('STACKED-BAR-CHART', 'Bar Chart (Stacked)'), ('LINE-CHART', 'Line Chart'), ('AREA-CHART', 'Area Chart'), ('PIE-CHART', 'Pie Chart'), ('TABLE', 'Table')], max_length=20),
        ),
        migrations.AlterField(
            model_name='schoolindicatordetaildataset',
            name='display_type',
            field=models.CharField(choices=[('BAR-CHART', 'Bar Chart'), ('BASIC-BAR-CHART', 'Bar Chart (Basic)'), ('STACKED-BAR-CHART', 'Bar Chart (Stacked)'), ('LINE-CHART', 'Line Chart'), ('AREA-CHART', 'Area Chart'), ('PIE-CHART', 'Pie Chart'), ('TABLE', 'Table')], max_length=20),
        ),
        migrations.AlterField(
            model_name='stateindicatordetaildataset',
            name='display_type',
            field=models.CharField(choices=[('BAR-CHART', 'Bar Chart'), ('BASIC-BAR-CHART', 'Bar Chart (Basic)'), ('STACKED-BAR-CHART', 'Bar Chart (Stacked)'), ('LINE-CHART', 'Line Chart'), ('AREA-CHART', 'Area Chart'), ('PIE-CHART', 'Pie Chart'), ('TABLE', 'Table')], max_length=20),
        ),
    ]
