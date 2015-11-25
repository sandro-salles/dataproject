# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='deleted_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='checkout',
            name='deleted_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='deleted_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
