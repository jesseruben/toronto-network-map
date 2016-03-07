# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NDT', '0012_auto_20160122_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ndt',
            name='price',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='ndtprofile',
            name='price',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True),
        ),
    ]
