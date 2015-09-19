# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_hstore.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=600, verbose_name='Nome', db_index=True)),
                ('json', django_hstore.fields.DictionaryField(null=True, editable=False)),
            ],
            options={
                'verbose_name': 'Cidade',
                'verbose_name_plural': 'Cidades',
            },
        ),
        migrations.CreateModel(
            name='Neighborhood',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=600, verbose_name='Nome', db_index=True)),
                ('json', django_hstore.fields.DictionaryField(null=True, editable=False)),
                ('city', models.ForeignKey(to='geo.City')),
            ],
            options={
                'verbose_name': 'Bairro',
                'verbose_name_plural': 'Bairro',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300, verbose_name='Nome', db_index=True)),
                ('abbreviation', models.CharField(max_length=2, verbose_name='Abrevia\xe7\xe3o', db_index=True)),
            ],
            options={
                'verbose_name': 'Estado',
                'verbose_name_plural': 'Estados',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(to='geo.State'),
        ),
    ]
