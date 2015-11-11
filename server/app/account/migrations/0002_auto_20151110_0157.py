# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='corporation',
            name='account',
        ),
        migrations.RemoveField(
            model_name='user',
            name='account',
        ),
        migrations.AddField(
            model_name='user',
            name='corporation',
            field=models.ForeignKey(blank=True, to='account.Corporation', null=True),
        ),
    ]
