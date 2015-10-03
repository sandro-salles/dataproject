# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
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
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_dirty', models.BooleanField(default=False, verbose_name='Inconsistente')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('contact_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='contact.Contact')),
                ('address', models.EmailField(max_length=254, verbose_name='E-mail')),
            ],
            options={
                'verbose_name': 'Endere\xe7o Eletr\xf4nico',
                'verbose_name_plural': 'Endere\xe7os Eletr\xf4nicos',
            },
            bases=('contact.contact',),
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('contact_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='contact.Contact')),
                ('country_code', models.CharField(default=b'+55', max_length=3, verbose_name='DDI', choices=[(b'+55', 'Brasil')])),
                ('type', models.CharField(max_length=3, verbose_name='Tipo do Aparelho', choices=[(b'cel', 'Celular'), (b'tel', 'Telefone Fixo')])),
                ('area_code', models.CharField(max_length=2, verbose_name='DDD')),
                ('number', models.CharField(max_length=9, verbose_name='N\xfamero')),
                ('hash', models.IntegerField(verbose_name='Hash', unique=True, editable=False, db_index=True)),
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
                ('hash', models.IntegerField(verbose_name='Hash', unique=True, editable=False, db_index=True)),
            ],
            options={
                'verbose_name': 'Endere\xe7o F\xedsico',
                'verbose_name_plural': 'Endere\xe7os F\xedsicos',
            },
            bases=('contact.contact',),
        ),
    ]
