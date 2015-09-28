# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=255, verbose_name='Email')),
                ('subject', models.CharField(max_length=100, verbose_name='Username')),
                ('message', models.CharField(max_length=40, verbose_name='Message Content')),
            ],
        ),
    ]
