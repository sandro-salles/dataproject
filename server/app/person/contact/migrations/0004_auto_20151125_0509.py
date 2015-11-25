# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0003_auto_20151125_0503'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='address',
            unique_together=set([('state', 'city', 'neighborhood', 'location', 'zipcode')]),
        ),
        migrations.AlterIndexTogether(
            name='address',
            index_together=set([('state', 'city', 'neighborhood'), ('state', 'city')]),
        ),
    ]
