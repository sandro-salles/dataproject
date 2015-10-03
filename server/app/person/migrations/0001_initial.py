# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reversion', '0002_auto_20141216_1509'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Cole\xe7\xe3o de Pessoas',
                'verbose_name_plural': 'Cole\xe7\xf5es de Pessoas',
            },
        ),
        migrations.CreateModel(
            name='CollectionItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('collection', models.ForeignKey(to='person.Collection')),
            ],
            options={
                'verbose_name': 'Item de Cole\xe7\xe3o de Pessoas',
                'verbose_name_plural': 'Itens de Cole\xe7\xe3o de Pessoas',
            },
        ),
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
        migrations.AddField(
            model_name='collectionitem',
            name='person',
            field=models.ForeignKey(to='person.Person'),
        ),
        migrations.AddField(
            model_name='collectionitem',
            name='revision',
            field=models.ForeignKey(to='reversion.Revision'),
        ),
        migrations.AddField(
            model_name='collection',
            name='persons',
            field=models.ManyToManyField(to='person.Person', through='person.CollectionItem'),
        ),
    ]
