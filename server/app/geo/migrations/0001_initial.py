# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True, db_column=b'loc_nu_sequencial')),
                ('name', models.CharField(max_length=50, null=True, db_column=b'loc_nosub', blank=True)),
                ('zipcode', models.CharField(max_length=16, null=True, db_column=b'cep', blank=True)),
            ],
            options={
                'db_table': 'log_localidade',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Neighborhood',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True, db_column=b'bai_nu_sequencial')),
                ('name', models.CharField(max_length=72, db_column=b'bai_no')),
                ('abbreviation', models.CharField(max_length=36, null=True, db_column=b'bai_no_abrev', blank=True)),
            ],
            options={
                'db_table': 'log_bairro',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NeighborhoodZipRange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fcb_nu_ordem', models.IntegerField()),
                ('fcb_rad_ini', models.CharField(max_length=5)),
                ('fcb_suf_ini', models.CharField(max_length=3)),
                ('fcb_rad_fim', models.CharField(max_length=5)),
                ('fcb_suf_fim', models.CharField(max_length=3)),
            ],
            options={
                'db_table': 'log_faixa_bairro',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.CharField(max_length=2, serialize=False, primary_key=True, db_column=b'ufe_sg')),
                ('name', models.CharField(max_length=72, db_column=b'ufe_no')),
                ('ufe_rad1_ini', models.CharField(max_length=5)),
                ('ufe_suf1_ini', models.CharField(max_length=3)),
                ('ufe_rad1_fim', models.CharField(max_length=5)),
                ('ufe_suf1_fim', models.CharField(max_length=3)),
                ('ufe_rad2_ini', models.CharField(max_length=5, null=True, blank=True)),
                ('ufe_suf2_ini', models.CharField(max_length=3, null=True, blank=True)),
                ('ufe_rad2_fim', models.CharField(max_length=5, null=True, blank=True)),
                ('ufe_suf2_fim', models.CharField(max_length=3, null=True, blank=True)),
            ],
            options={
                'db_table': 'log_faixa_uf',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Street',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True, db_column=b'log_nu_sequencial')),
                ('name', models.CharField(max_length=70, db_column=b'log_no')),
                ('zipcode', models.CharField(max_length=16, db_column=b'cep', db_index=True)),
                ('type', models.CharField(max_length=72, null=True, db_column=b'log_tipo_logradouro', blank=True)),
                ('normalized_name', models.CharField(max_length=70, db_column=b'log_no_sem_acento')),
            ],
            options={
                'db_table': 'log_logradouro',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CityZipRange',
            fields=[
                ('city', models.ForeignKey(primary_key=True, db_column=b'loc_nu_sequencial', serialize=False, to='geo.City')),
                ('loc_rad1_ini', models.CharField(max_length=5)),
                ('loc_suf1_ini', models.CharField(max_length=3)),
                ('loc_rad1_fim', models.CharField(max_length=5)),
                ('loc_suf1_fim', models.CharField(max_length=3)),
                ('loc_rad2_ini', models.CharField(max_length=5, null=True, blank=True)),
                ('loc_suf2_ini', models.CharField(max_length=3, null=True, blank=True)),
                ('loc_rad2_fim', models.CharField(max_length=5, null=True, blank=True)),
                ('loc_suf2_fim', models.CharField(max_length=3, null=True, blank=True)),
            ],
            options={
                'db_table': 'log_faixa_localidade',
                'managed': False,
            },
        ),
    ]
