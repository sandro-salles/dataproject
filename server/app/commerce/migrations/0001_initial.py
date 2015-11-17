# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields.ranges


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('contact', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('status', models.CharField(default=b'created', max_length=14, verbose_name='Status', db_index=True, choices=[(b'created', 'Criado'), (b'finished', 'Finalizado')])),
                ('account', models.ForeignKey(to='account.Account')),
            ],
            options={
                'verbose_name': 'Carrinho de compras',
                'verbose_name_plural': 'Carrinhos de compras',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('cart', models.ForeignKey(related_name='items', to='commerce.Cart')),
            ],
            options={
                'verbose_name': 'Item de Carrinho de compras',
                'verbose_name_plural': 'Itens de Carrinho de compras',
            },
        ),
        migrations.CreateModel(
            name='CheckoutCriteria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nature', models.CharField(max_length=1, verbose_name='Person Nature', db_index=True)),
                ('areacode', models.CharField(max_length=2, verbose_name='DDD', db_index=True)),
                ('city', models.CharField(max_length=200, verbose_name='Cidade', db_index=True)),
                ('neighborhood', models.CharField(max_length=200, verbose_name='Bairro', db_index=True)),
                ('carrier', models.ForeignKey(to='contact.Carrier')),
            ],
            options={
                'verbose_name': 'Criterio de sele\xe7\xe3o de dados',
                'verbose_name_plural': 'Criterios de sele\xe7\xe3o de dados',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'awaiting', max_length=14, verbose_name='Status', db_index=True, choices=[(b'awaiting', 'Em aberto'), (b'late', 'Atrasado'), (b'settled', 'Liquidado')])),
                ('total', models.FloatField(verbose_name='Valor total do pagamento')),
                ('ref_installment', models.IntegerField(default=1, verbose_name='Parcela de refer\xeancia')),
                ('settled_at', models.DateTimeField(verbose_name='Pago em')),
            ],
            options={
                'verbose_name': 'Pagamento',
                'verbose_name_plural': 'Pagamentos',
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
                ('total', models.FloatField(verbose_name='Valor total da compra')),
                ('price_per_unit', models.FloatField(verbose_name='Pre\xe7o por registro')),
                ('price_per_unit_range', django.contrib.postgres.fields.ranges.IntegerRangeField(verbose_name='Faixa de pre\xe7o por registro')),
                ('method', models.CharField(default=b'billet', max_length=14, verbose_name='M\xe9todo de pagamento', db_index=True, choices=[(b'billet', b'Boleto'), (b'deposit', b'Deposito')])),
                ('num_installments', models.IntegerField(default=1, verbose_name='N\xfamero de parcelas')),
                ('buyer', models.ForeignKey(to='account.AppUser')),
                ('cart', models.ForeignKey(to='commerce.Cart')),
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
            name='Checkout',
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
            model_name='purchaseitem',
            name='purchase',
            field=models.ForeignKey(related_name='items', to='commerce.Purchase'),
        ),
        migrations.AddField(
            model_name='purchasable',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_commerce.purchasable_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='purchase',
            field=models.ForeignKey(to='commerce.Purchase'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='purchasable',
            field=models.ForeignKey(to='commerce.Purchasable'),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('checkout_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='commerce.Checkout')),
            ],
            options={
                'verbose_name': 'Cruzamento de Dados',
                'verbose_name_plural': 'Cruzamentos de Dados',
            },
            bases=('commerce.checkout',),
        ),
        migrations.AddField(
            model_name='checkoutcriteria',
            name='checkout',
            field=models.ForeignKey(related_name='criteria', to='commerce.Checkout'),
        ),
    ]
