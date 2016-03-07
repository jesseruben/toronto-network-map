# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isp', '0002_auto_20150917_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='isp',
            name='phone',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='isp',
            name='support_phone',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
    ]
