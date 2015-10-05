# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number', models.CharField(max_length=20, null=True, verbose_name='N\xfamero', blank=True)),
                ('complement', models.CharField(max_length=50, null=True, verbose_name='Complemento', blank=True)),
                ('hash', models.IntegerField(verbose_name='Hash', unique=True, editable=False)),
            ],
            options={
                'verbose_name': 'Endere\xe7o F\xedsico',
                'verbose_name_plural': 'Endere\xe7os F\xedsicos',
            },
        ),
        migrations.CreateModel(
            name='Carrier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Nome', db_index=True)),
                ('slug', models.SlugField(null=True, max_length=200, blank=True, unique=True, verbose_name='Identificador')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Operadora de Telefonia',
                'verbose_name_plural': 'Operadoras de Telefonia',
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.EmailField(max_length=254, verbose_name='E-mail')),
            ],
            options={
                'verbose_name': 'Endere\xe7o Eletr\xf4nico',
                'verbose_name_plural': 'Endere\xe7os Eletr\xf4nicos',
            },
        ),
        migrations.CreateModel(
            name='PersonAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PersonEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PersonPhone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(max_length=3, verbose_name='Tipo do Aparelho', choices=[(b'cel', 'Celular'), (b'tel', 'Telefone Fixo')])),
                ('area_code', models.CharField(max_length=2, verbose_name='DDD')),
                ('number', models.CharField(max_length=9, verbose_name='N\xfamero')),
                ('hash', models.IntegerField(verbose_name='Hash', unique=True, editable=False)),
                ('carrier', models.ForeignKey(to='contact.Carrier')),
            ],
            options={
                'verbose_name': 'Telefone',
                'verbose_name_plural': 'Telefones',
            },
        ),
    ]
