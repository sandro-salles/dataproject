# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20151110_0157'),
        ('commerce', '0003_auto_20151110_0157'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Account',
        ),
    ]
