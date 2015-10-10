# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0001_initial'),
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='datacollection',
            name='collection',
            field=models.ForeignKey(to='person.Collection'),
        ),
        migrations.AddField(
            model_name='datacheckout',
            name='data_collection',
            field=models.ForeignKey(to='commerce.DataCollection'),
        ),
    ]
