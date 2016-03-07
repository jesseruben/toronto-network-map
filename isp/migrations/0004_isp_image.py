# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isp', '0003_auto_20151229_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='isp',
            name='image',
            field=models.ImageField(null=True, upload_to=b'', blank=True),
        ),
    ]
