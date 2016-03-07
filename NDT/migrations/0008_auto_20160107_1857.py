# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NDT', '0007_ndtprofile_isp_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ndtprofile',
            name='isp_name',
            field=models.CharField(help_text=b'Entered by the user when his ISP is not listed', max_length=64, null=True, blank=True),
        ),
    ]
