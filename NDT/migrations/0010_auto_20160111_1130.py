# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NDT', '0009_auto_20160108_1613'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='country',
        ),
        migrations.AlterField(
            model_name='ndt',
            name='service_type',
            field=models.CharField(default=b'Home', max_length=20, null=True, blank=True, choices=[(b'BUSINESS', 'Business'), (b'HOME', '\u0622\u063a\u0627\u0632\u0647'), (b'PUBLIC', 'Public')]),
        ),
        migrations.AlterField(
            model_name='ndtprofile',
            name='service_type',
            field=models.CharField(max_length=20, choices=[(b'BUSINESS', 'Business'), (b'HOME', '\u0622\u063a\u0627\u0632\u0647'), (b'PUBLIC', 'Public')]),
        ),
    ]
