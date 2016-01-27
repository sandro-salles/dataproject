# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('state', models.CharField(db_index=True, max_length=2, verbose_name='State', choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amap\xe1'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Cear\xe1'), ('DF', 'Distrito Federal'), ('ES', 'Esp\xedrito Santo'), ('GO', 'Goi\xe1s'), ('MA', 'Maranh\xe3o'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Par\xe1'), ('PB', 'Para\xedba'), ('PR', 'Paran\xe1'), ('PE', 'Pernambuco'), ('PI', 'Piau\xed'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rond\xf4nia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'S\xe3o Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')])),
                ('city', models.CharField(max_length=200, verbose_name='Cidade', db_index=True)),
                ('neighborhood', models.CharField(max_length=200, verbose_name='Bairro', db_index=True)),
                ('location', models.TextField(verbose_name='Endere\xe7o')),
                ('zipcode', models.CharField(max_length=8, verbose_name='CEP', db_index=True)),
            ],
            options={
                'verbose_name': 'Endere\xe7o F\xedsico',
                'verbose_name_plural': 'Endere\xe7os F\xedsicos',
            },
        ),
        migrations.CreateModel(
            name='Carrier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'Nome', db_index=True)),
                ('slug', models.SlugField(null=True, max_length=200, blank=True, unique=True, verbose_name=b'Identificador')),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('address', models.EmailField(unique=True, max_length=254, verbose_name='E-mail')),
            ],
            options={
                'verbose_name': 'Endere\xe7o Eletr\xf4nico',
                'verbose_name_plural': 'Endere\xe7os Eletr\xf4nicos',
            },
        ),
        migrations.CreateModel(
            name='PersonAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('address', models.ForeignKey(to='contact.Address')),
                ('person', models.ForeignKey(to='person.Person')),
            ],
        ),
        migrations.CreateModel(
            name='PersonEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('email', models.ForeignKey(to='contact.Email')),
                ('person', models.ForeignKey(to='person.Person')),
            ],
        ),
        migrations.CreateModel(
            name='PersonPhone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('person', models.ForeignKey(to='person.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('type', models.CharField(db_index=True, max_length=3, verbose_name='Tipo do Aparelho', choices=[(b'cel', 'Celular'), (b'tel', 'Telefone Fixo')])),
                ('areacode', models.IntegerField(db_index=True, verbose_name=' C\xf3digo DDD', choices=[(11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (21, 21), (22, 22), (24, 24), (27, 27), (28, 28), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (37, 37), (38, 38), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49), (51, 51), (53, 53), (54, 54), (55, 55), (61, 61), (62, 62), (63, 63), (64, 64), (65, 65), (66, 66), (67, 67), (68, 68), (69, 69), (71, 71), (73, 73), (74, 74), (75, 75), (77, 77), (79, 79), (81, 81), (82, 82), (83, 83), (84, 84), (85, 85), (86, 86), (87, 87), (88, 88), (89, 89), (91, 91), (92, 92), (93, 93), (94, 94), (95, 95), (96, 96), (97, 97), (98, 98), (99, 99)])),
                ('number', models.CharField(max_length=9, verbose_name='N\xfamero')),
                ('address', models.ForeignKey(to='contact.Address')),
                ('carrier', models.ForeignKey(to='contact.Carrier')),
                ('persons', models.ManyToManyField(related_name='phones', through='contact.PersonPhone', to='person.Person')),
            ],
            options={
                'verbose_name': 'Telefone',
                'verbose_name_plural': 'Telefones',
            },
        ),
        migrations.AddField(
            model_name='personphone',
            name='phone',
            field=models.ForeignKey(to='contact.Phone'),
        ),
        migrations.AddField(
            model_name='email',
            name='persons',
            field=models.ManyToManyField(to='person.Person', through='contact.PersonEmail'),
        ),
        migrations.AddField(
            model_name='address',
            name='persons',
            field=models.ManyToManyField(related_name='addresses', through='contact.PersonAddress', to='person.Person'),
        ),
        migrations.AlterUniqueTogether(
            name='phone',
            unique_together=set([('type', 'areacode', 'number')]),
        ),
        migrations.AlterIndexTogether(
            name='phone',
            index_together=set([('areacode', 'carrier'), ('areacode', 'carrier', 'address')]),
        ),
        migrations.AlterUniqueTogether(
            name='personphone',
            unique_together=set([('person', 'phone')]),
        ),
        migrations.AlterUniqueTogether(
            name='personemail',
            unique_together=set([('person', 'email')]),
        ),
        migrations.AlterUniqueTogether(
            name='personaddress',
            unique_together=set([('person', 'address')]),
        ),
        migrations.AlterUniqueTogether(
            name='address',
            unique_together=set([('state', 'city', 'neighborhood', 'location', 'zipcode')]),
        ),
        migrations.AlterIndexTogether(
            name='address',
            index_together=set([('state', 'city', 'neighborhood'), ('state', 'city')]),
        ),
    ]
