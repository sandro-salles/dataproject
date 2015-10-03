# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('geo', '0001_initial'),
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='persons',
            field=models.ManyToManyField(to='person.Person'),
        ),
        migrations.AddField(
            model_name='contact',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_contact.contact_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='physicaladdress',
            name='city',
            field=models.ForeignKey(to='geo.City'),
        ),
        migrations.AddField(
            model_name='physicaladdress',
            name='neighborhood',
            field=models.ForeignKey(to='geo.Neighborhood'),
        ),
        migrations.AddField(
            model_name='physicaladdress',
            name='state',
            field=models.ForeignKey(to='geo.State'),
        ),
        migrations.AddField(
            model_name='physicaladdress',
            name='street',
            field=models.ForeignKey(to='geo.Street'),
        ),
        migrations.AddField(
            model_name='phone',
            name='carrier',
            field=models.ForeignKey(to='contact.Carrier'),
        ),
        migrations.AlterUniqueTogether(
            name='physicaladdress',
            unique_together=set([('street', 'number', 'complement')]),
        ),
        migrations.AlterUniqueTogether(
            name='phone',
            unique_together=set([('type', 'area_code', 'number')]),
        ),
    ]
