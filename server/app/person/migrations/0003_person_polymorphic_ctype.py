# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('person', '0002_remove_person_polymorphic_ctype'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_person.person_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
    ]
