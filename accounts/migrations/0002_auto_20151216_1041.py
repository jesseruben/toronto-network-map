# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='log_guid',
            field=models.TextField(default=accounts.models._create_hash, unique=True, max_length=512, verbose_name='Globally Unique Identifier (GUID) for logging purposes'),
        ),
        migrations.AlterField(
            model_name='useruid',
            name='guid',
            field=models.TextField(unique=True, max_length=512, verbose_name='Globally Unique Identifier (GUID)'),
        ),
    ]
