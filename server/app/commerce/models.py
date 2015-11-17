# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from core.models import DatableModel
from account.models import Account, AppUser
from person.contact.models import Carrier
from polymorphic import PolymorphicModel
from person.models import Person

from django.contrib.postgres.fields import IntegerRangeField


PAYMENT_METHOD_CHOICES_BILLET = ('billet', 'Boleto')
PAYMENT_METHOD_CHOICES_DEPOSIT = ('deposit', 'Deposito')

PAYMENT_METHOD_CHOICES = (
    PAYMENT_METHOD_CHOICES_BILLET,
    PAYMENT_METHOD_CHOICES_DEPOSIT
)


class Purchasable(PolymorphicModel, DatableModel):

    class Meta:
        verbose_name = _('Produto')
        verbose_name_plural = _('Produtos')

    def __unicode__(self):
        return self.id


class Checkout(Purchasable):

    class Meta:
        verbose_name = _('Checkout de Dados')
        verbose_name_plural = _('Checkouts de Dados')

    def __unicode__(self):
        return self.id


class CheckoutCriteria(models.Model):

    checkout = models.ForeignKey(Checkout, related_name='criteria')
    nature = models.CharField(_(u'Person Nature'), max_length=1, db_index=True)
    carrier = models.ForeignKey(Carrier)
    areacode = models.CharField(_(u'DDD'), max_length=2, db_index=True)
    city = models.CharField(_(u'Cidade'), max_length=200, db_index=True)
    neighborhood = models.CharField(_(u'Bairro'), max_length=200, db_index=True)

    class Meta:
        verbose_name = _(u'Criterio de seleção de dados')
        verbose_name_plural = _(u'Criterios de seleção de dados')

    def __unicode__(self):
        return self.id


class Match(Checkout):

    class Meta:
        verbose_name = _('Cruzamento de Dados')
        verbose_name_plural = _('Cruzamentos de Dados')

    def __unicode__(self):
        return self.id


class Cart(DatableModel):

    STATUS_CHOICES_CREATED = ('created', _('Criado'))
    STATUS_CHOICES_FINISHED = ('finished', _('Finalizado'))
    STATUS_CHOICES = (STATUS_CHOICES_CREATED, STATUS_CHOICES_FINISHED)

    account = models.ForeignKey(Account)
    status = models.CharField(_('Status'), max_length=14, db_index=True,
                              choices=STATUS_CHOICES, default=STATUS_CHOICES_CREATED[0])

    class Meta:
        verbose_name = _('Carrinho de compras')
        verbose_name_plural = _('Carrinhos de compras')

    def __unicode__(self):
        return self.account


class CartItem(DatableModel):
    cart = models.ForeignKey(Cart, related_name='items')
    purchasable = models.ForeignKey(Purchasable)

    class Meta:
        verbose_name = _('Item de Carrinho de compras')
        verbose_name_plural = _('Itens de Carrinho de compras')

    def __unicode__(self):
        return self.cart


class Purchase(PolymorphicModel, DatableModel):

    cart = models.ForeignKey(Cart)
    buyer = models.ForeignKey(AppUser)

    total = models.FloatField(_('Valor total da compra'))
    price_per_unit = models.FloatField(_(u'Preço por registro'))
    price_per_unit_range = IntegerRangeField(_(u'Faixa de preço por registro'))

    method = models.CharField(_(u'Método de pagamento'), max_length=14, db_index=True,
                              choices=PAYMENT_METHOD_CHOICES, default=PAYMENT_METHOD_CHOICES_BILLET[0])
    num_installments = models.IntegerField(_(u'Número de parcelas'), default=1)

    class Meta:
        verbose_name = _('Compra')
        verbose_name_plural = _('Compra')

    def __unicode__(self):
        return self.cart


class PurchaseItem(PolymorphicModel, DatableModel):
    purchase = models.ForeignKey(Purchase, related_name='items')
    purchasable = models.ForeignKey(Purchasable)

    class Meta:
        verbose_name = _('Item de Compra')
        verbose_name_plural = _('Itens de Compra')

    def __unicode__(self):
        return self.collection


class Payment(models.Model):

    STATUS_CHOICES_AWAITING = ('awaiting', _('Em aberto'))
    STATUS_CHOICES_LATE = ('late', _('Atrasado'))
    STATUS_CHOICES_SETTLED = ('settled', _('Liquidado'))
    STATUS_CHOICES = (STATUS_CHOICES_AWAITING,
                      STATUS_CHOICES_LATE, STATUS_CHOICES_SETTLED)

    purchase = models.ForeignKey(Purchase)
    status = models.CharField(_('Status'), max_length=14, db_index=True,
                              choices=STATUS_CHOICES, default=STATUS_CHOICES_AWAITING[0])
    total = models.FloatField(_('Valor total do pagamento'))

    ref_installment = models.IntegerField(
        _(u'Parcela de referência'), default=1)
    settled_at = models.DateTimeField(_('Pago em'))

    class Meta:
        verbose_name = _('Pagamento')
        verbose_name_plural = _('Pagamentos')

    def __unicode__(self):
        return self.purchase
