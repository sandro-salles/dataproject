# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_auto_20151125_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='neighborhood',
            field=models.CharField(max_length=200, verbose_name='Bairro', db_index=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='zipcode',
            field=models.CharField(max_length=8, verbose_name='CEP', db_index=True),
        ),
    ]
