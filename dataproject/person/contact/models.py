# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings
from polymorphic import PolymorphicModel
from core.models import DatableModel, SlugModel
from person.models import Person
from geo.models import State, City, Neighborhood
from django_hstore import hstore
from core.util import sanitize_text

import reversion


class PhoneOperator(PolymorphicModel, SlugModel, DatableModel):

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


class Contact(PolymorphicModel, DatableModel):
    persons = models.ManyToManyField(Person)

    class Meta:
        verbose_name        = _("Contato")
        verbose_name_plural = _("Contato")

    def __unicode__(self):
        return self.person.name


class Phone(Contact):

    country_code = models.CharField(_('DDI'), max_length=3, default='+55')
    area_code = models.CharField(_('DDD'), max_length=2, db_index=True)
    number = models.CharField(_(u'Número'), max_length=9, db_index=True)

    json = hstore.DictionaryField(schema=[
        {
            'name': 'j_country_code',
            'class': 'CharField',
            'kwargs': {
                'blank': False,
                'max_length': 3,
            }
        },
        {
            'name': 'j_area_code',
            'class': 'CharField',
            'kwargs': {
                'blank': False,
                'max_length': 2,
            }
        },
        {
            'name': 'j_number',
            'class': 'CharField',
            'kwargs': {
                'blank': False,
                'max_length': 8,
            }
        },
        {
            'name': 'j_operator_name',
            'class': 'CharField',
            'kwargs': {
                'blank': False,
                'max_length': 300,
            }
        },
        {
            'name': 'j_use_type',
            'class': 'CharField',
            'kwargs': {
                'blank': True,
                'max_length': 50,
            }
        },
    ], editable=False)

    objects = hstore.HStoreManager()


    class Meta:
        verbose_name        = _("Telefone")
        verbose_name_plural = _("Telefones")
        unique_together     = (('area_code', 'number'), ('country_code', 'area_code', 'number'))

    def save(self, *args, **kwargs):
        self.json = {'j_country_code': self.country_code, 'j_area_code': self.area_code, 'j_number': self.number, }
        super(Telephone, self).save(*args, **kwargs)

@reversion.register
class Telephone(Phone):

    USE_TYPE_CHOICES_HOME       = ('res', _('Residencial'))
    USE_TYPE_CHOICES_COMMERCIAL = ('com', _('Comercial'))
    USE_TYPE_CHOICES_MESSAGES   = ('rec', _('Recados'))

    USE_TYPE_CHOICES            = (USE_TYPE_CHOICES_HOME, USE_TYPE_CHOICES_COMMERCIAL, USE_TYPE_CHOICES_MESSAGES)

    
    operator = models.ForeignKey(TelephoneOperator)
    use_type = models.CharField(_('Tipo de Uso'), db_index=True, max_length=50, choices=USE_TYPE_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name        = _("Telefone Fixo")
        verbose_name_plural = _("Telefones Fixos")

    def save(self, *args, **kwargs):
        self.json = {'j_operator_name': self.operator.name, 'j_use_type': self.use_type}
        super(Telephone, self).save(*args, **kwargs)


@reversion.register
class Cellphone(Phone):

    USE_TYPE_CHOICES_PERSONAL   = ('pes', _('Pessoal'))
    USE_TYPE_CHOICES_CORPORATE  = ('cor', _('Corporativo'))

    USE_TYPE_CHOICES            = (USE_TYPE_CHOICES_PERSONAL, USE_TYPE_CHOICES_CORPORATE)

    operator = models.ForeignKey(MobileOperator)
    use_type = models.CharField(_('Tipo de Uso'), db_index=True, max_length=50, choices=USE_TYPE_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name        = _("Telefone Celular")
        verbose_name_plural = _("Telefones Celular")

    def save(self, *args, **kwargs):
        self.json = {'j_operator_name': self.operator.name, 'j_use_type': self.use_type}
        super(Cellphone, self).save(*args, **kwargs)

@reversion.register
class PhysicalAddress(Contact):

    USE_TYPE_CHOICES_HOME       = ('res', _('Residencial'))
    USE_TYPE_CHOICES_COMMERCIAL = ('com', _('Comercial'))

    USE_TYPE_CHOICES            = (USE_TYPE_CHOICES_HOME, USE_TYPE_CHOICES_COMMERCIAL)

    state = models.ForeignKey(State)
    city = models.ForeignKey(City)
    neighborhood = models.ForeignKey(Neighborhood)

    address = models.TextField(_('Logradouro'), max_length=800)
    zipcode = models.CharField(_('CEP'), max_length=8)
    latitude = models.FloatField(_('Latitude'), db_index=True, blank=True, null=True)
    longitude = models.FloatField(_('Longitude'), db_index=True, blank=True, null=True)

    use_type = models.CharField(_('Tipo de Uso'), db_index=True, max_length=50, choices=USE_TYPE_CHOICES, blank=True, null=True)

    json = hstore.DictionaryField(schema=[
        {
            'name': 'j_state_name',
            'class': 'CharField',
            'kwargs': {
                'blank': False,
                'max_length': 300,
            }
        },
        {
            'name': 'j_state_abbreviation',
            'class': 'CharField',
            'kwargs': {
                'blank': False,
                'max_length': 2,
            }
        },
        {
            'name': 'j_city_name',
            'class': 'CharField',
            'kwargs': {
                'blank': False,
                'max_length': 600,
            }
        },
        {
            'name': 'j_neighborhood_name',
            'class': 'CharField',
            'kwargs': {
                'blank': False,
                'max_length': 600,
            }
        },
        {
            'name': 'j_address',
            'class': 'TextField',
            'kwargs': {
                'blank': False,
                'max_length': 800,
            }
        },
        {
            'name': 'j_zipcode',
            'class': 'CharField',
            'kwargs': {
                'blank': False,
                'max_length': 8,
            }
        },
        {
            'name': 'j_latitude',
            'class': 'FloatField',
            'kwargs': {
                'blank': True,
            }
        },
        {
            'name': 'j_longitude',
            'class': 'FloatField',
            'kwargs': {
                'blank': True,
            }
        },
        {
            'name': 'j_use_type',
            'class': 'CharField',
            'kwargs': {
                'blank': True,
                'max_length': 50,
            }
        },
    ], editable=False)

    objects = hstore.HStoreManager()

    class Meta:
        verbose_name        = _(u"Endereço Físico")
        verbose_name_plural = _(u"Endereços Físicos")

    def save(self, *args, **kwargs):

        self.address = sanitize_text(self.address)

        self.json = {
            'j_state_name': self.state.name, 
            'j_state_abbreviation': self.state.abbreviation, 
            'j_city_name': self.city.name, 
            'j_neighborhood_name': self.neighborhood.name, 
            'j_address': self.address,
            'j_zipcode': self.postal_code,
            'j_latitude': self.latitude,
            'j_longitude': self.longitude,
            'j_use_type': self.use_type,
        }

        super(PhysicalAddress, self).save(*args, **kwargs)


@reversion.register
class Email(Contact):

    USE_TYPE_CHOICES_PERSONAL   = ('pes', _('Pessoal'))
    USE_TYPE_CHOICES_CORPORATE  = ('cor', _('Corporativo'))

    USE_TYPE_CHOICES            = (USE_TYPE_CHOICES_PERSONAL, USE_TYPE_CHOICES_CORPORATE)

    address = models.EmailField(_('E-mail'))
    use_type = models.CharField(_('Tipo de Uso'), db_index=True, max_length=50, choices=USE_TYPE_CHOICES, blank=True, null=True)

    json = hstore.DictionaryField(schema=[
        {
            'name': 'j_address',
            'class': 'CharField',
            'kwargs': {
                'blank': False,
                'max_length': 600,
            }
        },
        {
            'name': 'j_use_type',
            'class': 'CharField',
            'kwargs': {
                'blank': True,
                'max_length': 50,
            }
        }
    ], editable=False)

    objects = hstore.HStoreManager()

    class Meta:
        verbose_name        = _(u"Endereço Eletrônico")
        verbose_name_plural = _(u"Endereços Eletrônicos")


    def save(self, *args, **kwargs):
        self.json = {
            'j_address': self.address,
            'j_use_type': self.use_type,
        }

        super(Email, self).save(*args, **kwargs)
    