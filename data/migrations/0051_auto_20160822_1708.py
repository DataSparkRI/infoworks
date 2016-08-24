# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-22 17:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0050_auto_20160527_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='districtovertime',
            name='stack_max',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='districtovertime',
            name='stack_min',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='schoolovertime',
            name='stack_max',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='schoolovertime',
            name='stack_min',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='stateovertime',
            name='stack_max',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='stateovertime',
            name='stack_min',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='districtdisplaydataydetailset',
            name='display_type',
            field=models.CharField(choices=[('BAR-CHART', 'Bar Chart'), ('BAR-CHART-ONLY', 'Bar Chart Only'), ('HORZ-BAR-CHART', 'Horizontal Bar Chart'), ('HORZ-BAR-CHART-ONLY', 'Horizontal Bar Chart Only'), ('LINE-CHART', 'Line Chart (under construction)'), ('AREA-CHART', 'Area Chart (under construction)'), ('PIE-CHART', 'Pie Chart'), ('TABLE', 'Table')], max_length=20),
        ),
        migrations.AlterField(
            model_name='districtindicatordetaildataset',
            name='display_type',
            field=models.CharField(choices=[('BAR-CHART', 'Bar Chart'), ('BAR-CHART-ONLY', 'Bar Chart Only'), ('HORZ-BAR-CHART', 'Horizontal Bar Chart'), ('HORZ-BAR-CHART-ONLY', 'Horizontal Bar Chart Only'), ('LINE-CHART', 'Line Chart (under construction)'), ('AREA-CHART', 'Area Chart (under construction)'), ('PIE-CHART', 'Pie Chart'), ('TABLE', 'Table')], max_length=20),
        ),
        migrations.AlterField(
            model_name='districtovertime',
            name='chart_type',
            field=models.CharField(choices=[('BAR-CHART', 'Bar Chart'), ('BAR-CHART-ONLY', 'Bar Chart Only'), ('HORZ-BAR-CHART', 'Horizontal Bar Chart'), ('HORZ-BAR-CHART-ONLY', 'Horizontal Bar Chart Only'), ('LINE-CHART', 'Line Chart (under construction)'), ('AREA-CHART', 'Area Chart (under construction)'), ('PIE-CHART', 'Pie Chart'), ('TABLE', 'Table')], default='BAR-CHART', max_length=50),
        ),
        migrations.AlterField(
            model_name='schooldisplaydataydetailset',
            name='display_type',
            field=models.CharField(choices=[('BAR-CHART', 'Bar Chart'), ('BAR-CHART-ONLY', 'Bar Chart Only'), ('HORZ-BAR-CHART', 'Horizontal Bar Chart'), ('HORZ-BAR-CHART-ONLY', 'Horizontal Bar Chart Only'), ('LINE-CHART', 'Line Chart (under construction)'), ('AREA-CHART', 'Area Chart (under construction)'), ('PIE-CHART', 'Pie Chart'), ('TABLE', 'Table')], max_length=20),
        ),
        migrations.AlterField(
            model_name='schoolindicatordetaildataset',
            name='display_type',
            field=models.CharField(choices=[('BAR-CHART', 'Bar Chart'), ('BAR-CHART-ONLY', 'Bar Chart Only'), ('HORZ-BAR-CHART', 'Horizontal Bar Chart'), ('HORZ-BAR-CHART-ONLY', 'Horizontal Bar Chart Only'), ('LINE-CHART', 'Line Chart (under construction)'), ('AREA-CHART', 'Area Chart (under construction)'), ('PIE-CHART', 'Pie Chart'), ('TABLE', 'Table')], max_length=20),
        ),
        migrations.AlterField(
            model_name='schoolovertime',
            name='chart_type',
            field=models.CharField(choices=[('BAR-CHART', 'Bar Chart'), ('BAR-CHART-ONLY', 'Bar Chart Only'), ('HORZ-BAR-CHART', 'Horizontal Bar Chart'), ('HORZ-BAR-CHART-ONLY', 'Horizontal Bar Chart Only'), ('LINE-CHART', 'Line Chart (under construction)'), ('AREA-CHART', 'Area Chart (under construction)'), ('PIE-CHART', 'Pie Chart'), ('TABLE', 'Table')], default='BAR-CHART', max_length=50),
        ),
        migrations.AlterField(
            model_name='statedisplaydataydetailset',
            name='display_type',
            field=models.CharField(choices=[('BAR-CHART', 'Bar Chart'), ('BAR-CHART-ONLY', 'Bar Chart Only'), ('HORZ-BAR-CHART', 'Horizontal Bar Chart'), ('HORZ-BAR-CHART-ONLY', 'Horizontal Bar Chart Only'), ('LINE-CHART', 'Line Chart (under construction)'), ('AREA-CHART', 'Area Chart (under construction)'), ('PIE-CHART', 'Pie Chart'), ('TABLE', 'Table')], max_length=20),
        ),
        migrations.AlterField(
            model_name='stateindicatordetaildataset',
            name='display_type',
            field=models.CharField(choices=[('BAR-CHART', 'Bar Chart'), ('BAR-CHART-ONLY', 'Bar Chart Only'), ('HORZ-BAR-CHART', 'Horizontal Bar Chart'), ('HORZ-BAR-CHART-ONLY', 'Horizontal Bar Chart Only'), ('LINE-CHART', 'Line Chart (under construction)'), ('AREA-CHART', 'Area Chart (under construction)'), ('PIE-CHART', 'Pie Chart'), ('TABLE', 'Table')], max_length=20),
        ),
        migrations.AlterField(
            model_name='stateovertime',
            name='chart_type',
            field=models.CharField(choices=[('BAR-CHART', 'Bar Chart'), ('BAR-CHART-ONLY', 'Bar Chart Only'), ('HORZ-BAR-CHART', 'Horizontal Bar Chart'), ('HORZ-BAR-CHART-ONLY', 'Horizontal Bar Chart Only'), ('LINE-CHART', 'Line Chart (under construction)'), ('AREA-CHART', 'Area Chart (under construction)'), ('PIE-CHART', 'Pie Chart'), ('TABLE', 'Table')], default='BAR-CHART', max_length=50),
        ),
    ]
