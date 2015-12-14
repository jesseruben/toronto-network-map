# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import NDT.models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
        ('isp', '0002_auto_20150917_1203'),
    ]

    operations = [
        migrations.CreateModel(
            name='NDT',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('download_rate', models.FloatField(verbose_name=b'Actual Download Rate (Kb)')),
                ('upload_rate', models.FloatField(verbose_name=b'Actual Upload Rate (Kb)')),
                ('nominal_download_rate', models.FloatField(null=True, verbose_name=b'Theoretical Download Rate(Kb)', blank=True)),
                ('nominal_upload_rate', models.FloatField(null=True, verbose_name=b'Theoretical Upload Rate (Kb)', blank=True)),
                ('latency', models.DecimalField(default=0, max_digits=6, decimal_places=3)),
                ('latitude', models.DecimalField(null=True, max_digits=8, decimal_places=5, blank=True)),
                ('longitude', models.DecimalField(null=True, max_digits=8, decimal_places=5, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('bandwidth', models.IntegerField(null=True, verbose_name=b'internet bandwidth (KB)', blank=True)),
                ('price', models.DecimalField(null=True, max_digits=7, decimal_places=2, blank=True)),
                ('city', models.CharField(max_length=64, null=True)),
                ('isp_name', models.CharField(max_length=64, null=True)),
                ('service_type', models.CharField(default=b'Home', max_length=20, null=True, blank=True, choices=[(b'BUSINESS', 'Business'), (b'HOME', 'Home'), (b'PUBLIC', 'Public')])),
                ('province', models.CharField(max_length=64, null=True)),
                ('rating_general', models.PositiveSmallIntegerField(null=True, verbose_name=b'general rating', blank=True)),
                ('hash', models.CharField(default=NDT.models._create_hash, unique=True, max_length=100, verbose_name=b'unique hash value used for UI identification')),
                ('average_index', models.DecimalField(default=1, verbose_name=b'Number of test results contributing to the average', max_digits=5, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='NDTProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('latitude', models.DecimalField(null=True, max_digits=8, decimal_places=5, blank=True)),
                ('longitude', models.DecimalField(null=True, max_digits=8, decimal_places=5, blank=True)),
                ('nominal_download_rate', models.DecimalField(null=True, verbose_name=b'nominal download rate', max_digits=6, decimal_places=3, blank=True)),
                ('nominal_upload_rate', models.DecimalField(null=True, verbose_name=b'nominal upload rate', max_digits=6, decimal_places=3, blank=True)),
                ('bandwidth', models.IntegerField(null=True, verbose_name=b'internet bandwidth', blank=True)),
                ('price', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('contract', models.BooleanField(default=False, verbose_name=b'on contract?')),
                ('service_type', models.CharField(max_length=20, choices=[(b'BUSINESS', 'Business'), (b'HOME', 'Home'), (b'PUBLIC', 'Public')])),
                ('vpn', models.NullBooleanField()),
                ('rating_general', models.PositiveSmallIntegerField(null=True, verbose_name=b'general rating', blank=True)),
                ('rating_customer_service', models.PositiveSmallIntegerField(null=True, verbose_name=b'customer service rating', blank=True)),
                ('province', models.CharField(max_length=64, null=True)),
                ('city', models.CharField(max_length=64, null=True)),
                ('promotion', models.NullBooleanField()),
                ('active', models.BooleanField(default=True)),
                ('country', models.ForeignKey(to='locations.Country', null=True)),
                ('isp', models.ForeignKey(to='isp.ISP')),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name='Server Name')),
                ('url', models.URLField(max_length=500, verbose_name='Server URL')),
                ('active', models.BooleanField(default=True, verbose_name='Server Active')),
                ('country', models.ForeignKey(verbose_name='Country Name', to='locations.Country')),
            ],
        ),
        migrations.CreateModel(
            name='Web100',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('blob', models.TextField()),
                ('ndt', models.ForeignKey(to='NDT.NDT')),
            ],
        ),
    ]
