# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NDT', '0006_auto_20160107_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='ndtprofile',
            name='isp_name',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
    ]
