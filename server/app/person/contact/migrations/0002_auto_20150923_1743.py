# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
        ('geo', '0001_initial'),
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='physicaladdress',
            name='persons',
            field=models.ManyToManyField(to='person.Person'),
        ),
        migrations.AddField(
            model_name='physicaladdress',
            name='street',
            field=models.ForeignKey(to='geo.Street'),
        ),
        migrations.AddField(
            model_name='phone',
            name='operator',
            field=models.ForeignKey(to='contact.PhoneOperator'),
        ),
        migrations.AddField(
            model_name='phone',
            name='persons',
            field=models.ManyToManyField(to='person.Person'),
        ),
        migrations.AddField(
            model_name='email',
            name='persons',
            field=models.ManyToManyField(to='person.Person'),
        ),
        migrations.AlterUniqueTogether(
            name='physicaladdress',
            unique_together=set([('street', 'number', 'complement')]),
        ),
        migrations.AlterUniqueTogether(
            name='phone',
            unique_together=set([('country_code', 'area_code', 'number')]),
        ),
    ]
