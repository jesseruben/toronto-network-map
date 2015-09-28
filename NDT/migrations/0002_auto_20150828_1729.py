# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
        ('NDT', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('isp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='country',
            field=models.ForeignKey(verbose_name='Country Name', to='locations.Country'),
        ),
        migrations.AddField(
            model_name='ndtprofile',
            name='country',
            field=models.ForeignKey(to='locations.Country', null=True),
        ),
        migrations.AddField(
            model_name='ndtprofile',
            name='isp',
            field=models.ForeignKey(to='isp.ISP'),
        ),
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
