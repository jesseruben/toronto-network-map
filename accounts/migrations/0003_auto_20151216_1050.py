# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20151216_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useruid',
            name='guid',
            field=models.TextField(default=accounts.models._create_hash, unique=True, max_length=512, verbose_name='Globally Unique Identifier (GUID)'),
        ),
    ]
