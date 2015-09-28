# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import NDT.models


class Migration(migrations.Migration):

    dependencies = [
        ('NDT', '0007_auto_20150921_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ndt',
            name='average_index',
            field=models.DecimalField(default=1, verbose_name=b'Number of test results contributing to the average', max_digits=5, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='ndt',
            name='hash',
            field=models.CharField(default=NDT.models._createhash, unique=True, max_length=100, verbose_name=b'unique hash value used for UI identification'),
        ),
    ]
