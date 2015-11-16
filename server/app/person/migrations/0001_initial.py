# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('is_dirty', models.BooleanField(default=False, verbose_name=b'Inconsistente')),
                ('name', models.CharField(max_length=300, verbose_name='Nome', db_index=True)),
                ('nature', models.CharField(db_index=True, max_length=3, verbose_name='Natureza', choices=[(b'P', 'F\xedsica'), (b'L', 'Jur\xeddica')])),
                ('document', models.CharField(unique=True, max_length=14, verbose_name='Documento')),
            ],
            options={
                'verbose_name': 'Pessoa',
                'verbose_name_plural': 'Pessoas',
            },
        ),
    ]
