# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from core.models import DatableModel
from account.models import Corporation
from polymorphic import PolymorphicModel
from person.models import Person


class Purchasable(PolymorphicModel, DatableModel):

    class Meta:
        verbose_name = _('Produto')
        verbose_name_plural = _('Produtos')

    def __unicode__(self):
        return self.id


class DataCollection(models.Model):
    persons = models.ManyToManyField(Person, through='DataCollectionItem')

    class Meta:
        verbose_name = _(u'Coleção de Dados')
        verbose_name_plural = _(u'Coleção de Dados')

    def __unicode__(self):
        return self.id


class DataCollectionItem(models.Model):
    person = models.ForeignKey(Person)
    collection = models.ForeignKey(DataCollection)
    

    class Meta:
        verbose_name = _(u"Item de Coleção de Dados")
        verbose_name_plural = _(u"Itens de Coleção de Dados")
        unique_together = ('person', 'collection',)

    def __unicode__(self):
        return self.person


class DataCheckout(Purchasable):
    collection = models.ForeignKey(DataCollection)

    class Meta:
        verbose_name = _('Checkout de Dados')
        verbose_name_plural = _('Checkouts de Dados')

    def __unicode__(self):
        return self.id


class DataMatch(DataCheckout):

    class Meta:
        verbose_name = _('Cruzamento de Dados')
        verbose_name_plural = _('Cruzamentos de Dados')

    def __unicode__(self):
        return self.id


class Purchase(PolymorphicModel, DatableModel):
    corporation = models.ForeignKey(Corporation)

    class Meta:
        verbose_name = _('Compra')
        verbose_name_plural = _('Compra')

    def __unicode__(self):
        return self.account


class PurchaseItem(PolymorphicModel, DatableModel):
    purchasable = models.ForeignKey(Purchasable)

    class Meta:
        verbose_name = _('Item de Compra')
        verbose_name_plural = _('Itens de Compra')

    def __unicode__(self):
        return self.collection
