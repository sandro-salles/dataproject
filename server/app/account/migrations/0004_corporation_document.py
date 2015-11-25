# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20151125_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporation',
            name='document',
            field=models.CharField(default='doc', max_length=14),
            preserve_default=False,
        ),
    ]
