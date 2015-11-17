# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddressCity',
            fields=[
                ('city', models.CharField(max_length=300, serialize=False, verbose_name='Cidade', primary_key=True)),
            ],
            options={
                'db_table': 'contact_address_city',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ContactAddressCityContactAddressNeighborhood',
            fields=[
                ('id', models.CharField(max_length=300, serialize=False, verbose_name='Id', primary_key=True)),
                ('city', models.CharField(max_length=200, verbose_name='Cidade', db_index=True)),
                ('neighborhood', models.CharField(max_length=200, verbose_name='Bairro', db_index=True)),
            ],
            options={
                'db_table': 'contact_address_city_contact_address_neighborhood',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ContactPhoneAreacodeContactAddressCity',
            fields=[
                ('id', models.CharField(max_length=300, serialize=False, verbose_name='Id', primary_key=True)),
                ('areacode', models.CharField(max_length=2, verbose_name='DDD')),
                ('city', models.CharField(max_length=200, verbose_name='Cidade', db_index=True)),
            ],
            options={
                'db_table': 'contact_phone_areacode_contact_address_city',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ContactPhoneCarrierContactPhoneAreacode',
            fields=[
                ('id', models.CharField(max_length=300, serialize=False, verbose_name='Id', primary_key=True)),
                ('areacode', models.CharField(max_length=2, verbose_name='DDD')),
            ],
            options={
                'db_table': 'contact_phone_carrier_contact_phone_areacode',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PersonNatureContactPhoneCarrier',
            fields=[
                ('id', models.CharField(max_length=300, serialize=False, verbose_name='Id', primary_key=True)),
                ('nature', models.CharField(max_length=1, verbose_name='Person Nature', db_index=True)),
            ],
            options={
                'db_table': 'person_nature_contact_phone_carrier',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PhoneAreacode',
            fields=[
                ('areacode', models.CharField(max_length=2, serialize=False, verbose_name='DDD', primary_key=True)),
            ],
            options={
                'db_table': 'contact_phone_areacode',
                'managed': False,
            },
        ),
    ]
