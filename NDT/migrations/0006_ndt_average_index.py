# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NDT', '0005_auto_20150921_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='ndt',
            name='average_index',
            field=models.DecimalField(default=0, max_digits=2, decimal_places=2),
        ),
    ]
