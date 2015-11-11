# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_delete_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporation',
            name='owner',
            field=models.ForeignKey(related_name='owned_corporation', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='corporation',
            field=models.ForeignKey(default=1, to='account.Corporation'),
            preserve_default=False,
        ),
    ]
