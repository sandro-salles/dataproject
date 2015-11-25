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
                ('total', models.FloatField(null=True, verbose_name='Valor total da compra', blank=True)),
                ('price_per_unit', models.FloatField(verbose_name='Pre\xe7o por registro', null=True, editable=False, blank=True)),
                ('price_per_unit_range', django.contrib.postgres.fields.ranges.IntegerRangeField(verbose_name='Faixa de pre\xe7o por registro', null=True, editable=False, blank=True)),
                ('account', models.ForeignKey(to='account.Account')),
            ],
            options={
                'verbose_name': 'Carrinho de compras',
                'verbose_name_plural': 'Carrinhos de compras',
            },
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Checkout de Dados',
                'verbose_name_plural': 'Checkouts de Dados',
            },
        ),
        migrations.CreateModel(
            name='CheckoutCriteria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nature', models.CharField(db_index=True, max_length=1, null=True, verbose_name='Person Nature', blank=True)),
                ('areacode', models.CharField(db_index=True, max_length=2, null=True, verbose_name='DDD', blank=True)),
                ('city', models.CharField(db_index=True, max_length=200, null=True, verbose_name='Cidade', blank=True)),
                ('neighborhood', models.CharField(db_index=True, max_length=200, null=True, verbose_name='Bairro', blank=True)),
                ('count', models.IntegerField(verbose_name='Total de registros \xfanicos', editable=False)),
                ('carrier', models.ForeignKey(blank=True, to='contact.Carrier', null=True)),
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
                ('buyer', models.ForeignKey(to='account.User')),
                ('cart', models.ForeignKey(to='commerce.Cart')),
            ],
            options={
                'verbose_name': 'Compra',
                'verbose_name_plural': 'Compra',
            },
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
            model_name='purchase',
            name='items',
            field=models.ManyToManyField(to='commerce.Checkout'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_commerce.purchase_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='purchase',
            field=models.ForeignKey(to='commerce.Purchase'),
        ),
        migrations.AddField(
            model_name='checkoutcriteria',
            name='checkout',
            field=models.ForeignKey(related_name='criteria', to='commerce.Checkout'),
        ),
        migrations.AddField(
            model_name='checkout',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_commerce.checkout_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(to='commerce.Checkout'),
        ),
    ]
