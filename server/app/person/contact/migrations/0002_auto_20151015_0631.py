# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
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
            name='persons',
            field=models.ManyToManyField(to='person.Person', through='contact.PersonAddress'),
        ),
        migrations.AlterUniqueTogether(
            name='phone',
            unique_together=set([('type', 'areacode', 'number')]),
        ),
        migrations.AlterUniqueTogether(
            name='personphone',
            unique_together=set([('person', 'phone')]),
        ),
        migrations.AlterUniqueTogether(
            name='personemail',
            unique_together=set([('person', 'email')]),
        ),
        migrations.AlterUniqueTogether(
            name='personaddress',
            unique_together=set([('person', 'address')]),
        ),
    ]
