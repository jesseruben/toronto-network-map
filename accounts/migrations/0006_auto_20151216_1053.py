# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20151216_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useruid',
            name='guid',
            field=models.TextField(unique=True, max_length=512, verbose_name='Globally Unique Identifier (GUID)'),
        ),
        migrations.AlterField(
            model_name='useruid',
            name='type',
            field=models.CharField(default=b'forgotPassword', max_length=50, verbose_name='Type', choices=[(b'forgotPassword', 'Forgot Password'), (b'activation', 'User Activation')]),
        ),
    ]
