# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Corporation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('slug', models.SlugField(null=True, max_length=200, blank=True, unique=True, verbose_name='Slug')),
                ('description', models.CharField(max_length=400, null=True, verbose_name='Description', blank=True)),
            ],
            options={
                'verbose_name': 'Corporation',
                'verbose_name_plural': 'Corporations',
            },
        ),
    ]
