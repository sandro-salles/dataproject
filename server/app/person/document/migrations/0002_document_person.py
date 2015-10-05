# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0001_initial'),
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='person',
            field=models.ForeignKey(to='person.Person'),
        ),
    ]
