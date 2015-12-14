# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('NDT', '0001_initial'),
        ('locations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='ndtprofile',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='ndt',
            name='country',
            field=models.ForeignKey(to='locations.Country', null=True),
        ),
        migrations.AddField(
            model_name='ndt',
            name='ndt_profile',
            field=models.ForeignKey(to='NDT.NDTProfile', null=True),
        ),
    ]
