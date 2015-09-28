# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NDT', '0006_ndt_average_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ndt',
            name='average_index',
            field=models.DecimalField(default=0, max_digits=5, decimal_places=2),
        ),
    ]
