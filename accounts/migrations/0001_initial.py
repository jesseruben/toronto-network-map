# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import accounts.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='Email', db_index=True)),
                ('username', models.CharField(unique=True, max_length=40, verbose_name='Username')),
                ('is_active', models.BooleanField(default=True, verbose_name='Only active user can login in the frontend')),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='The time when the user was created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last time user got update')),
                ('notifications', models.IntegerField(default=0, verbose_name='Number of new notifications')),
                ('log_guid', models.CharField(default=accounts.models._create_hash, unique=True, max_length=100, verbose_name='Globally Unique Identifier (GUID) for logging purposes')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserUID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('guid', models.CharField(unique=True, max_length=100, verbose_name='Globally Unique Identifier (GUID)')),
                ('expiration_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Expiration Date')),
                ('type', models.CharField(default=b'forgotPassword', max_length=1, verbose_name='Type', choices=[(b'forgotPassword', 'Forgot Password'), (b'activation', 'User Activation')])),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
