# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150912_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporation',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 18, 44, 25, 618336, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='corporation',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 12, 18, 44, 32, 802355, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
