# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_hstore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Contato',
                'verbose_name_plural': 'Contato',
            },
        ),
        migrations.CreateModel(
            name='PhoneOperator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Nome')),
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
                ('contact_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='contact.Contact')),
                ('address', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('use_type', models.CharField(choices=[(b'pes', 'Pessoal'), (b'cor', 'Corporativo')], max_length=50, blank=True, null=True, verbose_name='Tipo de Uso', db_index=True)),
                ('json', django_hstore.fields.DictionaryField(null=True, editable=False)),
            ],
            options={
                'verbose_name': 'Endere\xe7o Eletr\xf4nico',
                'verbose_name_plural': 'Endere\xe7os Eletr\xf4nicos',
            },
            bases=('contact.contact',),
        ),
        migrations.CreateModel(
            name='MobileOperator',
            fields=[
                ('phoneoperator_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='contact.PhoneOperator')),
            ],
            options={
                'verbose_name': 'Operadora de Telefonia Celular',
                'verbose_name_plural': 'Operadoras de Telefonia Celular',
            },
            bases=('contact.phoneoperator',),
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('contact_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='contact.Contact')),
                ('country_code', models.CharField(default=b'+55', max_length=3, verbose_name='DDI', db_index=True)),
                ('area_code', models.CharField(max_length=2, verbose_name='DDD', db_index=True)),
                ('number', models.CharField(max_length=9, verbose_name='N\xfamero', db_index=True)),
                ('json', django_hstore.fields.DictionaryField(null=True, editable=False)),
            ],
            options={
                'verbose_name': 'Telefone',
                'verbose_name_plural': 'Telefones',
            },
            bases=('contact.contact',),
        ),
        migrations.CreateModel(
            name='PhysicalAddress',
            fields=[
                ('contact_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='contact.Contact')),
                ('number', models.CharField(max_length=20, null=True, verbose_name='N\xfamero', blank=True)),
                ('complement', models.CharField(max_length=50, null=True, verbose_name='Complemento', blank=True)),
                ('latitude', models.FloatField(db_index=True, null=True, verbose_name='Latitude', blank=True)),
                ('longitude', models.FloatField(db_index=True, null=True, verbose_name='Longitude', blank=True)),
                ('use_type', models.CharField(choices=[(b'res', 'Residencial'), (b'com', 'Comercial')], max_length=50, blank=True, null=True, verbose_name='Tipo de Uso', db_index=True)),
                ('json', django_hstore.fields.DictionaryField(null=True, editable=False)),
            ],
            options={
                'verbose_name': 'Endere\xe7o F\xedsico',
                'verbose_name_plural': 'Endere\xe7os F\xedsicos',
            },
            bases=('contact.contact',),
        ),
        migrations.CreateModel(
            name='TelephoneOperator',
            fields=[
                ('phoneoperator_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='contact.PhoneOperator')),
            ],
            options={
                'verbose_name': 'Operadora de Telefonia Fixa',
                'verbose_name_plural': 'Operadoras de Telefonia Fixa',
            },
            bases=('contact.phoneoperator',),
        ),
        migrations.AddField(
            model_name='phoneoperator',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_contact.phoneoperator_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
    ]
