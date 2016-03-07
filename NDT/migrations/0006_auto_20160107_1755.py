# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NDT', '0005_auto_20151223_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ndtprofile',
            name='isp',
            field=models.ForeignKey(blank=True, to='isp.ISP', null=True),
        ),
    ]
