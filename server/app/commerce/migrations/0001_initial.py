# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('reversion', '0002_auto_20141216_1509'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Cole\xe7\xe3o de Dados',
                'verbose_name_plural': 'Cole\xe7\xe3o de Dados',
            },
        ),
        migrations.CreateModel(
            name='DataCollectionItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('collection', models.ForeignKey(to='commerce.DataCollection')),
                ('person', models.ForeignKey(to='person.Person')),
                ('revision', models.ForeignKey(to='reversion.Revision')),
            ],
            options={
                'verbose_name': 'Item de Cole\xe7\xe3o de Dados',
                'verbose_name_plural': 'Itens de Cole\xe7\xe3o de Dados',
            },
        ),
        migrations.CreateModel(
            name='Purchasable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('corporation', models.ForeignKey(to='account.Corporation')),
                ('polymorphic_ctype', models.ForeignKey(related_name='polymorphic_commerce.purchase_set+', editable=False, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'verbose_name': 'Compra',
                'verbose_name_plural': 'Compra',
            },
        ),
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('polymorphic_ctype', models.ForeignKey(related_name='polymorphic_commerce.purchaseitem_set+', editable=False, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'verbose_name': 'Item de Compra',
                'verbose_name_plural': 'Itens de Compra',
            },
        ),
        migrations.CreateModel(
            name='DataCheckout',
            fields=[
                ('purchasable_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='commerce.Purchasable')),
            ],
            options={
                'verbose_name': 'Checkout de Dados',
                'verbose_name_plural': 'Checkouts de Dados',
            },
            bases=('commerce.purchasable',),
        ),
        migrations.AddField(
            model_name='purchaseitem',
            name='purchasable',
            field=models.ForeignKey(to='commerce.Purchasable'),
        ),
        migrations.AddField(
            model_name='purchasable',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_commerce.purchasable_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='datacollection',
            name='persons',
            field=models.ManyToManyField(to='person.Person', through='commerce.DataCollectionItem'),
        ),
        migrations.CreateModel(
            name='DataMatch',
            fields=[
                ('datacheckout_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='commerce.DataCheckout')),
            ],
            options={
                'verbose_name': 'Cruzamento de Dados',
                'verbose_name_plural': 'Cruzamentos de Dados',
            },
            bases=('commerce.datacheckout',),
        ),
        migrations.AlterUniqueTogether(
            name='datacollectionitem',
            unique_together=set([('person', 'collection', 'revision')]),
        ),
        migrations.AddField(
            model_name='datacheckout',
            name='collection',
            field=models.ForeignKey(to='commerce.DataCollection'),
        ),
    ]
