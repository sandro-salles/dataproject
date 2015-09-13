# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactendpoint',
            name='person',
            field=models.ForeignKey(to='person.Person'),
        ),
        migrations.AddField(
            model_name='contactendpoint',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_contact.contactendpoint_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(to='contact.State'),
        ),
        migrations.CreateModel(
            name='Cellphone',
            fields=[
                ('phone_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='contact.Phone')),
                ('number', models.CharField(max_length=9, verbose_name='N\xfamero')),
                ('use_type', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tipo de Uso', choices=[(b'pes', 'Pessoal'), (b'cor', 'Corporativo')])),
                ('operator', models.ForeignKey(to='contact.MobileOperator')),
            ],
            options={
                'verbose_name': 'Telefone Celular',
                'verbose_name_plural': 'Telefones Celular',
            },
            bases=('contact.phone',),
        ),
        migrations.CreateModel(
            name='Telephone',
            fields=[
                ('phone_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='contact.Phone')),
                ('number', models.CharField(max_length=8, verbose_name='N\xfamero')),
                ('use_type', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tipo de Uso', choices=[(b'res', 'Residencial'), (b'com', 'Comercial'), (b'rec', 'Recados')])),
                ('operator', models.ForeignKey(to='contact.TelephoneOperator')),
            ],
            options={
                'verbose_name': 'Telefone Fixo',
                'verbose_name_plural': 'Telefones Fixos',
            },
            bases=('contact.phone',),
        ),
        migrations.AddField(
            model_name='physicaladdress',
            name='city',
            field=models.ForeignKey(to='contact.City'),
        ),
        migrations.AddField(
            model_name='physicaladdress',
            name='neighborhood',
            field=models.ForeignKey(to='contact.Neighborhood'),
        ),
        migrations.AddField(
            model_name='physicaladdress',
            name='state',
            field=models.ForeignKey(to='contact.State'),
        ),
    ]
