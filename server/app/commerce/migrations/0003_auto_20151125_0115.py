# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0002_auto_20151125_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkoutcriteria',
            name='state',
            field=models.CharField(db_index=True, max_length=2, null=True, verbose_name='Estado', blank=True),
        ),
        migrations.AlterField(
            model_name='checkoutcriteria',
            name='nature',
            field=models.CharField(db_index=True, max_length=1, null=True, verbose_name='Natureza', blank=True),
        ),
    ]
