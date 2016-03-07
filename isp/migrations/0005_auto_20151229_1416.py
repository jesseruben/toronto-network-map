# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isp', '0004_isp_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='isp',
            name='image',
            field=models.ImageField(null=True, upload_to=b'img/isps/', blank=True),
        ),
    ]
