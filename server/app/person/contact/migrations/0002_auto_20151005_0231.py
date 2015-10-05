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
            model_name='phone',
            name='persons',
            field=models.ManyToManyField(to='person.Person', through='contact.PersonPhone'),
        ),
        migrations.AddField(
            model_name='personphone',
            name='person',
            field=models.ForeignKey(to='person.Person'),
        ),
        migrations.AddField(
            model_name='personphone',
            name='phone',
            field=models.ForeignKey(to='contact.Phone'),
        ),
        migrations.AddField(
            model_name='personemail',
            name='email',
            field=models.ForeignKey(to='contact.Email'),
        ),
        migrations.AddField(
            model_name='personemail',
            name='person',
            field=models.ForeignKey(to='person.Person'),
        ),
        migrations.AddField(
            model_name='personaddress',
            name='address',
            field=models.ForeignKey(to='contact.Address'),
        ),
        migrations.AddField(
            model_name='personaddress',
            name='person',
            field=models.ForeignKey(to='person.Person'),
        ),
        migrations.AddField(
            model_name='email',
            name='persons',
            field=models.ManyToManyField(to='person.Person', through='contact.PersonEmail'),
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(to='geo.City'),
        ),
        migrations.AddField(
            model_name='address',
            name='neighborhood',
            field=models.ForeignKey(to='geo.Neighborhood'),
        ),
        migrations.AddField(
            model_name='address',
            name='persons',
            field=models.ManyToManyField(to='person.Person', through='contact.PersonAddress'),
        ),
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.ForeignKey(to='geo.State'),
        ),
        migrations.AddField(
            model_name='address',
            name='street',
            field=models.ForeignKey(to='geo.Street'),
        ),
        migrations.AlterUniqueTogether(
            name='phone',
            unique_together=set([('type', 'area_code', 'number')]),
        ),
        migrations.AlterUniqueTogether(
            name='address',
            unique_together=set([('street', 'number', 'complement')]),
        ),
    ]
