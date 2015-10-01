# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CNPJ',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_dirty', models.BooleanField(default=False, verbose_name='Inconsistente')),
                ('number', models.CharField(unique=True, max_length=14, verbose_name='N\xfamero', db_index=True)),
            ],
            options={
                'verbose_name': 'CNPJ',
                'verbose_name_plural': "CNPJ's",
            },
        ),
        migrations.CreateModel(
            name='CPF',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_dirty', models.BooleanField(default=False, verbose_name='Inconsistente')),
                ('number', models.CharField(unique=True, max_length=11, verbose_name='N\xfamero', db_index=True)),
            ],
            options={
                'verbose_name': 'CPF',
                'verbose_name_plural': "CPF's",
            },
        ),
        migrations.CreateModel(
            name='RG',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_dirty', models.BooleanField(default=False, verbose_name='Inconsistente')),
                ('number', models.CharField(unique=True, max_length=20, verbose_name='N\xfamero', db_index=True)),
                ('issuer', models.CharField(max_length=300, verbose_name='\xd3rg\xe3o Emissor')),
            ],
            options={
                'verbose_name': 'RG',
                'verbose_name_plural': "RG's",
            },
        ),
    ]
