# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NDT', '0004_auto_20150921_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ndt',
            name='latency',
            field=models.DecimalField(default=0, max_digits=6, decimal_places=3),
        ),
    ]
