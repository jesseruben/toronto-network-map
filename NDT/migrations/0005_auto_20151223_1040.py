# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NDT', '0004_auto_20151216_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ndtprofile',
            name='isp',
            field=models.ForeignKey(to='isp.ISP', null=True),
        ),
    ]
