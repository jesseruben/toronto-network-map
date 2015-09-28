# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import cities_light.abstract_models


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_ascii', models.CharField(db_index=True, max_length=200, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', editable=False)),
                ('geoname_id', models.IntegerField(unique=True, null=True, blank=True)),
                ('alternate_names', models.TextField(default=b'', null=True, blank=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('display_name', models.CharField(max_length=200)),
                ('search_names', cities_light.abstract_models.ToSearchTextField(default=b'', max_length=4000, db_index=True, blank=True)),
                ('latitude', models.DecimalField(null=True, max_digits=8, decimal_places=5, blank=True)),
                ('longitude', models.DecimalField(null=True, max_digits=8, decimal_places=5, blank=True)),
                ('population', models.BigIntegerField(db_index=True, null=True, blank=True)),
                ('feature_code', models.CharField(db_index=True, max_length=10, null=True, blank=True)),
                ('localized_name', models.CharField(max_length=64, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name_plural': 'cities',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_ascii', models.CharField(db_index=True, max_length=200, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', editable=False)),
                ('geoname_id', models.IntegerField(unique=True, null=True, blank=True)),
                ('alternate_names', models.TextField(default=b'', null=True, blank=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('code2', models.CharField(max_length=2, unique=True, null=True, blank=True)),
                ('code3', models.CharField(max_length=3, unique=True, null=True, blank=True)),
                ('continent', models.CharField(db_index=True, max_length=2, choices=[(b'OC', 'Oceania'), (b'EU', 'Europe'), (b'AF', 'Africa'), (b'NA', 'North America'), (b'AN', 'Antarctica'), (b'SA', 'South America'), (b'AS', 'Asia')])),
                ('tld', models.CharField(db_index=True, max_length=5, blank=True)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('localized_name', models.CharField(max_length=64, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name_plural': 'countries',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_ascii', models.CharField(db_index=True, max_length=200, blank=True)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', editable=False)),
                ('geoname_id', models.IntegerField(unique=True, null=True, blank=True)),
                ('alternate_names', models.TextField(default=b'', null=True, blank=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('display_name', models.CharField(max_length=200)),
                ('geoname_code', models.CharField(db_index=True, max_length=50, null=True, blank=True)),
                ('localized_name', models.CharField(max_length=64, null=True)),
                ('country', models.ForeignKey(related_name='locations_region_country', to='cities_light.Country')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'region/state',
                'verbose_name_plural': 'regions/states',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(related_name='locations_city_country', to='cities_light.Country'),
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.ForeignKey(related_name='locations_city_region', blank=True, to='cities_light.Region', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='region',
            unique_together=set([('country', 'name'), ('country', 'slug')]),
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set([('region', 'name'), ('region', 'slug')]),
        ),
    ]
