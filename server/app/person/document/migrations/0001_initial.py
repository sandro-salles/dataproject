# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(max_length=6, verbose_name='Tipo do Documento', choices=[(b'CPF', 'CPF'), (b'RG', 'RG'), (b'CNPJ', 'CNPJ')])),
                ('number', models.CharField(unique=True, max_length=30, verbose_name='N\xfamero')),
                ('issuer', models.CharField(max_length=300, verbose_name='\xd3rg\xe3o Emissor', blank=True)),
                ('hash', models.IntegerField(verbose_name='Hash', unique=True, editable=False)),
            ],
            options={
                'verbose_name': 'Documento Pessoal',
                'verbose_name_plural': 'Documentos Pessoais',
            },
        ),
    ]
