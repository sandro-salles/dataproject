# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
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
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(to='account.Account')),
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
                ('updated_at', models.DateTimeField(auto_now=True)),
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
                ('product_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='commerce.Product')),
            ],
            options={
                'verbose_name': 'Checkout de Dados',
                'verbose_name_plural': 'Checkouts de Dados',
            },
            bases=('commerce.product',),
        ),
        migrations.CreateModel(
            name='DataCollection',
            fields=[
                ('product_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='commerce.Product')),
            ],
            options={
                'verbose_name': 'Cole\xe7\xe3o de Dados',
                'verbose_name_plural': 'Cole\xe7\xe3o de Dados',
            },
            bases=('commerce.product',),
        ),
        migrations.CreateModel(
            name='DataMatch',
            fields=[
                ('product_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='commerce.Product')),
                ('data_collection', models.ForeignKey(to='commerce.DataCollection')),
            ],
            options={
                'verbose_name': 'Cruzamento de Dados',
                'verbose_name_plural': 'Cruzamentos de Dados',
            },
            bases=('commerce.product',),
        ),
        migrations.AddField(
            model_name='purchaseitem',
            name='product',
            field=models.ForeignKey(to='commerce.Product'),
        ),
        migrations.AddField(
            model_name='product',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_commerce.product_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
    ]
