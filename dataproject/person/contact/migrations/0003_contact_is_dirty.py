# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_auto_20150922_0259'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='is_dirty',
            field=models.BooleanField(default=False, verbose_name='Inconsistente'),
        ),
    ]
