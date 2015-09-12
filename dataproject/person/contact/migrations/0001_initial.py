# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=600, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Cidade',
                'verbose_name_plural': 'Cidades',
            },
        ),
        migrations.CreateModel(
            name='ContactEndpoint',
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
            name='Neighborhood',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=600, verbose_name='Nome')),
                ('city', models.ForeignKey(to='contact.City')),
            ],
            options={
                'verbose_name': 'Bairro',
                'verbose_name_plural': 'Bairro',
            },
        ),
        migrations.CreateModel(
            name='PhoneOperator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=300, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Operadora de Telefonia',
                'verbose_name_plural': 'Operadoras de Telefonia',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300, verbose_name='Nome')),
                ('abbreviation', models.CharField(max_length=2, verbose_name='Abrevia\xe7\xe3o')),
            ],
            options={
                'verbose_name': 'Estado',
                'verbose_name_plural': 'Estados',
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('contactendpoint_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='contact.ContactEndpoint')),
                ('address', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('use_type', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tipo de Uso', choices=[(b'pes', 'Pessoal'), (b'cor', 'Corporativo')])),
            ],
            options={
                'verbose_name': 'Endere\xe7o Eletr\xf4nico',
                'verbose_name_plural': 'Endere\xe7os Eletr\xf4nicos',
            },
            bases=('contact.contactendpoint',),
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
                ('contactendpoint_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='contact.ContactEndpoint')),
                ('country_code', models.CharField(default=b'+55', max_length=3, verbose_name='DDI')),
                ('area_code', models.CharField(max_length=2, verbose_name='DDD')),
            ],
            options={
                'verbose_name': 'Telefone',
                'verbose_name_plural': 'Telefones',
            },
            bases=('contact.contactendpoint',),
        ),
        migrations.CreateModel(
            name='PhysicalAddress',
            fields=[
                ('contactendpoint_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='contact.ContactEndpoint')),
                ('address', models.CharField(max_length=600, verbose_name='Logradouro')),
                ('postal_code', models.CharField(max_length=8, verbose_name='CEP')),
                ('latitude', models.FloatField(null=True, verbose_name='Latitude', blank=True)),
                ('longitude', models.FloatField(null=True, verbose_name='Longitude', blank=True)),
                ('use_type', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tipo de Uso', choices=[(b'res', 'Residencial'), (b'com', 'Comercial')])),
            ],
            options={
                'verbose_name': 'Endere\xe7o F\xedsico',
                'verbose_name_plural': 'Endere\xe7os F\xedsicos',
            },
            bases=('contact.contactendpoint',),
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
