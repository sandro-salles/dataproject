# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('geo', '0001_initial'),
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='persons',
            field=models.ManyToManyField(to='person.Person'),
        ),
        migrations.AddField(
            model_name='contact',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_contact.contact_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.CreateModel(
            name='Cellphone',
            fields=[
                ('phone_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='contact.Phone')),
                ('use_type', models.CharField(choices=[(b'pes', 'Pessoal'), (b'cor', 'Corporativo')], max_length=50, blank=True, null=True, verbose_name='Tipo de Uso', db_index=True)),
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
                ('use_type', models.CharField(choices=[(b'res', 'Residencial'), (b'com', 'Comercial'), (b'rec', 'Recados')], max_length=50, blank=True, null=True, verbose_name='Tipo de Uso', db_index=True)),
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
            field=models.ForeignKey(to='geo.City'),
        ),
        migrations.AddField(
            model_name='physicaladdress',
            name='neighborhood',
            field=models.ForeignKey(to='geo.Neighborhood'),
        ),
        migrations.AddField(
            model_name='physicaladdress',
            name='state',
            field=models.ForeignKey(to='geo.State'),
        ),
        migrations.AlterUniqueTogether(
            name='phone',
            unique_together=set([('area_code', 'number'), ('country_code', 'area_code', 'number')]),
        ),
    ]
