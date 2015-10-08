# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Nome', db_index=True)),
                ('slug', models.SlugField(null=True, max_length=200, blank=True, unique=True, verbose_name='Identificador')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Conta',
                'verbose_name_plural': 'Contas',
            },
        ),
        migrations.CreateModel(
            name='Corporation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Nome', db_index=True)),
                ('slug', models.SlugField(null=True, max_length=200, blank=True, unique=True, verbose_name='Identificador')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(to='account.Account')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Nome', db_index=True)),
                ('slug', models.SlugField(null=True, max_length=200, blank=True, unique=True, verbose_name='Identificador')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Usu\xe1rio',
                'verbose_name_plural': 'Usu\xe1rios',
            },
        ),
        migrations.CreateModel(
            name='CorporateUser',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='account.User')),
                ('corporation', models.ForeignKey(to='account.Corporation')),
            ],
            options={
                'verbose_name': 'Usu\xe1rio Corporativo',
                'verbose_name_plural': 'Usu\xe1rios Corporativos',
            },
            bases=('account.user',),
        ),
        migrations.AddField(
            model_name='user',
            name='account',
            field=models.ForeignKey(to='account.Account'),
        ),
        migrations.AddField(
            model_name='user',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_account.user_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
    ]
