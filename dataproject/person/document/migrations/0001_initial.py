# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number', models.CharField(max_length=20, verbose_name='N\xfamero', db_index=True)),
            ],
            options={
                'verbose_name': 'Documento Pessoal',
                'verbose_name_plural': 'Documentos Pessoais',
            },
        ),
        migrations.CreateModel(
            name='LegalPersonDocument',
            fields=[
                ('persondocument_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='document.PersonDocument')),
            ],
            options={
                'verbose_name': 'Documento de Pessoa Jur\xeddica',
                'verbose_name_plural': 'Documentos de Pessoa Jur\xeddica',
            },
            bases=('document.persondocument',),
        ),
        migrations.CreateModel(
            name='PhysicalPersonDocument',
            fields=[
                ('persondocument_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='document.PersonDocument')),
            ],
            options={
                'verbose_name': 'Documento de Pessoa F\xedsica',
                'verbose_name_plural': 'Documentos de Pessoa F\xedsica',
            },
            bases=('document.persondocument',),
        ),
        migrations.AddField(
            model_name='persondocument',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_document.persondocument_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.CreateModel(
            name='CNPJ',
            fields=[
                ('legalpersondocument_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='document.LegalPersonDocument')),
            ],
            options={
                'verbose_name': 'CNPJ',
                'verbose_name_plural': "CNPJ's",
            },
            bases=('document.legalpersondocument',),
        ),
        migrations.CreateModel(
            name='CPF',
            fields=[
                ('physicalpersondocument_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='document.PhysicalPersonDocument')),
            ],
            options={
                'verbose_name': 'CPF',
                'verbose_name_plural': "CPF's",
            },
            bases=('document.physicalpersondocument',),
        ),
        migrations.CreateModel(
            name='RG',
            fields=[
                ('physicalpersondocument_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='document.PhysicalPersonDocument')),
                ('issuer', models.CharField(max_length=300, verbose_name='\xd3rg\xe3o Emissor')),
            ],
            options={
                'verbose_name': 'RG',
                'verbose_name_plural': "RG's",
            },
            bases=('document.physicalpersondocument',),
        ),
    ]
