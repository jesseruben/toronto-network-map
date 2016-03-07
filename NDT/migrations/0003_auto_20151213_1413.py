# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('NDT', '0002_auto_20151213_1402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ndt',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='ndt',
            name='longitude',
        ),
        migrations.AddField(
            model_name='ndt',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True),
        ),
    ]
