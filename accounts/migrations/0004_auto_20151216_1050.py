# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20151216_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useruid',
            name='guid',
            field=models.TextField(unique=True, max_length=512, verbose_name='Globally Unique Identifier (GUID)'),
        ),
    ]
