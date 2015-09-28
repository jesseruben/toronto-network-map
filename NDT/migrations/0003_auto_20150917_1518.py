# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NDT', '0002_auto_20150828_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ndt',
            name='service_type',
            field=models.CharField(default=b'Home', max_length=20, null=True, blank=True, choices=[(b'BUSINESS', 'Business'), (b'HOME', 'Home'), (b'PUBLIC', 'Public')]),
        ),
    ]
