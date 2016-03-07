# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isp', '0005_auto_20151229_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='isp',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='isp',
            name='support_link',
            field=models.URLField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='isp',
            name='twitter',
            field=models.URLField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='isp',
            name='website',
            field=models.URLField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='plan',
            name='download_rate',
            field=models.DecimalField(max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='plan',
            name='link',
            field=models.URLField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='name',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='price',
            field=models.DecimalField(max_digits=10, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='plan',
            name='upload_rate',
            field=models.DecimalField(max_digits=10, decimal_places=4),
        ),
    ]
