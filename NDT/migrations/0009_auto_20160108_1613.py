# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import NDT.models


class Migration(migrations.Migration):

    dependencies = [
        ('NDT', '0008_auto_20160107_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='ndtprofile',
            name='hash',
            field=models.TextField(db_index=True, max_length=512, null=True, verbose_name=b'hash value used for UI identification', blank=True),
        ),
        migrations.AlterField(
            model_name='ndt',
            name='hash',
            field=models.TextField(default=NDT.models._create_hash, unique=True, max_length=512, verbose_name=b'unique hash value used for UI identification', db_index=True),
        ),
    ]
