# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_dirty', models.BooleanField(default=False, verbose_name='Inconsistente')),
                ('name', models.CharField(max_length=300, verbose_name='Nome', db_index=True)),
            ],
            options={
                'verbose_name': 'Pessoa',
                'verbose_name_plural': 'Pessoas',
            },
        ),
        migrations.CreateModel(
            name='LegalPerson',
            fields=[
                ('person_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='person.Person')),
            ],
            options={
                'verbose_name': 'Pessoa Jur\xeddica',
                'verbose_name_plural': 'Pessoas Jur\xeddicas',
            },
            bases=('person.person',),
        ),
        migrations.CreateModel(
            name='PhysicalPerson',
            fields=[
                ('person_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='person.Person')),
            ],
            options={
                'verbose_name': 'Pessoa F\xedsica',
                'verbose_name_plural': 'Pessoas F\xedsicas',
            },
            bases=('person.person',),
        ),
        migrations.AddField(
            model_name='person',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_person.person_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
    ]
