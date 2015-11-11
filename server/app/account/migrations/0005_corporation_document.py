# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20151110_0206'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporation',
            name='document',
            field=models.CharField(default=11111111111111, unique=True, max_length=14, verbose_name=b'CNPJ'),
            preserve_default=False,
        ),
    ]
