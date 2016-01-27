# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.IntegerField(serialize=False, verbose_name='Id', primary_key=True)),
                ('nature', models.CharField(max_length=1, verbose_name='Natureza da pessoa', db_index=True)),
                ('state', models.CharField(max_length=1, verbose_name='Estado', db_index=True)),
                ('areacode', models.CharField(max_length=2, verbose_name='DDD', db_index=True)),
                ('city', models.CharField(max_length=200, verbose_name='Cidade', db_index=True)),
                ('neighborhood', models.CharField(max_length=200, verbose_name='Bairro', db_index=True)),
            ],
            options={
                'db_table': 'materialized_filter',
                'managed': False,
            },
        ),
    ]
