# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NDT', '0003_auto_20150917_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ndt',
            name='download_rate',
            field=models.FloatField(verbose_name=b'Actual Download Rate (Kb)'),
        ),
        migrations.AlterField(
            model_name='ndt',
            name='nominal_download_rate',
            field=models.FloatField(null=True, verbose_name=b'Theoretical Download Rate(Kb)', blank=True),
        ),
        migrations.AlterField(
            model_name='ndt',
            name='nominal_upload_rate',
            field=models.FloatField(null=True, verbose_name=b'Theoretical Upload Rate (Kb)', blank=True),
        ),
        migrations.AlterField(
            model_name='ndt',
            name='upload_rate',
            field=models.FloatField(verbose_name=b'Actual Upload Rate (Kb)'),
        ),
    ]
