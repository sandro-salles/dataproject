# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='corporation',
        ),
        migrations.AddField(
            model_name='appuser',
            name='corporation',
            field=models.ForeignKey(default=1, to='account.Corporation'),
            preserve_default=False,
        ),
    ]
