# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import NDT.models


class Migration(migrations.Migration):

    dependencies = [
        ('NDT', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ndt',
            name='hash',
            field=models.CharField(default=NDT.models._create_hash, unique=True, max_length=500, verbose_name=b'unique hash value used for UI identification'),
        ),
    ]
