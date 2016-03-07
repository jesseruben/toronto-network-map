# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NDT', '0010_auto_20160111_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='url',
            field=models.CharField(max_length=500, verbose_name='Server URL'),
        ),
    ]
