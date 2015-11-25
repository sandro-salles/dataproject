# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0004_auto_20151125_0509'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='phone',
            index_together=set([('areacode', 'carrier'), ('areacode', 'carrier', 'address')]),
        ),
    ]
