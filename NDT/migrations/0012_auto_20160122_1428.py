# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NDT', '0011_auto_20160111_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ndtprofile',
            name='price',
            field=models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True),
        ),
    ]
