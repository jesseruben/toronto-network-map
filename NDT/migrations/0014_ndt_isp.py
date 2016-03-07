# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isp', '0006_auto_20160120_1410'),
        ('NDT', '0013_auto_20160126_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='ndt',
            name='isp',
            field=models.ForeignKey(blank=True, to='isp.ISP', null=True),
        ),
    ]
