# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('isp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='price',
            field=models.DecimalField(max_digits=7, decimal_places=2),
        ),
    ]
