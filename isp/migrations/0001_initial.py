# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ISP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('website', models.URLField(max_length=500)),
                ('phone', models.IntegerField()),
                ('support_phone', models.IntegerField(null=True, blank=True)),
                ('rating', models.FloatField(max_length=3, blank=True)),
                ('facebook', models.URLField(max_length=500, null=True, blank=True)),
                ('twitter', models.URLField(max_length=500, null=True, blank=True)),
                ('support_link', models.URLField(max_length=500, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, null=True, blank=True)),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('contract', models.BooleanField(default=False)),
                ('contract_length', models.IntegerField(null=True, blank=True)),
                ('download_rate', models.DecimalField(max_digits=6, decimal_places=3)),
                ('upload_rate', models.DecimalField(max_digits=6, decimal_places=3)),
                ('bandwidth', models.BooleanField(default=True)),
                ('bandwidth_limit', models.IntegerField(null=True, blank=True)),
                ('limited_offer', models.BooleanField(default=False)),
                ('link', models.URLField(max_length=50, null=True, blank=True)),
                ('isp', models.ForeignKey(related_name='plans', to='isp.ISP')),
            ],
        ),
    ]
