# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='datacollectionitem',
            unique_together=set([('person', 'collection')]),
        ),
        migrations.RemoveField(
            model_name='datacollectionitem',
            name='revision',
        ),
    ]
