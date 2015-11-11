# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20151110_0157'),
        ('commerce', '0002_auto_20151110_0140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='account',
        ),
        migrations.AddField(
            model_name='purchase',
            name='corporation',
            field=models.ForeignKey(default=1, to='account.Corporation'),
            preserve_default=False,
        ),
    ]
