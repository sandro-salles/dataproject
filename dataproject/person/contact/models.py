# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings
from polymorphic import PolymorphicModel
from core.models import DatableModel
from person.models import Person


class PhoneOperator(PolymorphicModel, DatableModel):
    name = models.CharField(_('Nome'), max_length=300)

    class Meta:
        verbose_name        = _("Operadora de Telefonia")
        verbose_name_plural = _("Operadoras de Telefonia")

    def __unicode__(self):
        return self.name


class TelephoneOperator(PhoneOperator):

    class Meta:
        verbose_name        = _("Operadora de Telefonia Fixa")
        verbose_name_plural = _("Operadoras de Telefonia Fixa")


class MobileOperator(PhoneOperator):

    class Meta:
        verbose_name        = _("Operadora de Telefonia Celular")
        verbose_name_plural = _("Operadoras de Telefonia Celular")


class ContactEndpoint(PolymorphicModel, DatableModel):
    person = models.ForeignKey(Person)

    class Meta:
        verbose_name        = _("Contato")
        verbose_name_plural = _("Contato")

    def __unicode__(self):
        return self.person.name


class Phone(ContactEndpoint):
    
    PURPOSE_RESIDENTIAL = ('res', _('Residencial'))

    country_code = models.CharField(_('DDI'), max_length=3, default='+55')
    area_code = models.CharField(_('DDD'), max_length=2)


    class Meta:
        verbose_name        = _("Telefone")
        verbose_name_plural = _("Telefones")


class Telephone(Phone):

    USE_TYPE_CHOICES_HOME       = ('res', _('Residencial'))
    USE_TYPE_CHOICES_COMMERCIAL = ('com', _('Comercial'))
    USE_TYPE_CHOICES_MESSAGES   = ('rec', _('Recados'))

    USE_TYPE_CHOICES            = (USE_TYPE_CHOICES_HOME, USE_TYPE_CHOICES_COMMERCIAL, USE_TYPE_CHOICES_MESSAGES)


    number = models.CharField(_(u'Número'), max_length=8)
    operator = models.ForeignKey(TelephoneOperator)
    use_type = models.CharField(_('Tipo de Uso'), max_length=50, choices=USE_TYPE_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name        = _("Telefone Fixo")
        verbose_name_plural = _("Telefones Fixos")


class Cellphone(Phone):

    USE_TYPE_CHOICES_PERSONAL   = ('pes', _('Pessoal'))
    USE_TYPE_CHOICES_CORPORATE  = ('cor', _('Corporativo'))

    USE_TYPE_CHOICES            = (USE_TYPE_CHOICES_PERSONAL, USE_TYPE_CHOICES_CORPORATE)

    number = models.CharField(_(u'Número'), max_length=9)
    operator = models.ForeignKey(MobileOperator)
    use_type = models.CharField(_('Tipo de Uso'), max_length=50, choices=USE_TYPE_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name        = _("Telefone Celular")
        verbose_name_plural = _("Telefones Celular")


class State(models.Model):
    name = models.CharField(_('Nome'), max_length=300)
    abbreviation = models.CharField(_(u'Abreviação'), max_length=2)

    class Meta:
        verbose_name        = _("Estado")
        verbose_name_plural = _("Estados")

    def __unicode__(self):
        return self.name


class City(models.Model):
    state = models.ForeignKey(State)
    name = models.CharField(_('Nome'), max_length=600)

    class Meta:
        verbose_name        = _("Cidade")
        verbose_name_plural = _("Cidades")

    def __unicode__(self):
        return self.name


class Neighborhood(models.Model):
    city = models.ForeignKey(City)
    name = models.CharField(_('Nome'), max_length=600)

    class Meta:
        verbose_name        = _("Bairro")
        verbose_name_plural = _("Bairro")

    def __unicode__(self):
        return self.name


class PhysicalAddress(ContactEndpoint):

    USE_TYPE_CHOICES_HOME       = ('res', _('Residencial'))
    USE_TYPE_CHOICES_COMMERCIAL = ('com', _('Comercial'))

    USE_TYPE_CHOICES            = (USE_TYPE_CHOICES_HOME, USE_TYPE_CHOICES_COMMERCIAL)

    state = models.ForeignKey(State)
    city = models.ForeignKey(City)
    neighborhood = models.ForeignKey(Neighborhood)

    address = models.CharField(_('Logradouro'), max_length=600)
    postal_code = models.CharField(_('CEP'), max_length=8)
    latitude = models.FloatField(_('Latitude'), blank=True, null=True)
    longitude = models.FloatField(_('Longitude'), blank=True, null=True)

    use_type = models.CharField(_('Tipo de Uso'), max_length=50, choices=USE_TYPE_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name        = _(u"Endereço Físico")
        verbose_name_plural = _(u"Endereços Físicos")


class Email(ContactEndpoint):

    USE_TYPE_CHOICES_PERSONAL   = ('pes', _('Pessoal'))
    USE_TYPE_CHOICES_CORPORATE  = ('cor', _('Corporativo'))

    USE_TYPE_CHOICES            = (USE_TYPE_CHOICES_PERSONAL, USE_TYPE_CHOICES_CORPORATE)

    address = models.EmailField(_('E-mail'))
    use_type = models.CharField(_('Tipo de Uso'), max_length=50, choices=USE_TYPE_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name        = _(u"Endereço Eletrônico")
        verbose_name_plural = _(u"Endereços Eletrônicos")



    