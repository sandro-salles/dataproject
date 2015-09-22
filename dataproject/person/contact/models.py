# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings
from polymorphic import PolymorphicModel
from core.models import DatableModel, SlugModel, DirtyModel
from person.models import Person
from geo.models import Street
from django_hstore import hstore
from person.contact.util import normalize_address

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


class Contact(PolymorphicModel, DatableModel, DirtyModel):
    persons = models.ManyToManyField(Person)

    class Meta:
        verbose_name        = _("Contato")
        verbose_name_plural = _("Contato")

    def __unicode__(self):
        return self.pk or ''


class Phone(Contact):

    COUNTRY_CODE_CHOICES_BRAZIL = '+55'

    country_code = models.CharField(_('DDI'), max_length=3, default=COUNTRY_CODE_CHOICES_BRAZIL, db_index=True)
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
        super(Phone, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s %s %s' % (self.country_code, self.area_code, self.number)

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

    street = models.ForeignKey(Street)
    number = models.CharField(_(u'Número'), max_length=20, blank=True, null=True)
    complement = models.CharField(_(u'Complemento'), max_length=50, blank=True, null=True)
    
    latitude = models.FloatField(_('Latitude'), db_index=True, blank=True, null=True)
    longitude = models.FloatField(_('Longitude'), db_index=True, blank=True, null=True)

    use_type = models.CharField(_('Tipo de Uso'), db_index=True, max_length=50, choices=USE_TYPE_CHOICES, blank=True, null=True)

    json = hstore.DictionaryField(schema=[
        {
            'name': 'j_street_name',
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
            'name': 'j_number',
            'class': 'CharField',
            'kwargs': {
                'blank': False,
                'max_length': 20,
            }
        },
        {
            'name': 'j_complement',
            'class': 'CharField',
            'kwargs': {
                'blank': False,
                'max_length': 50,
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

        self.json = {
            'j_state_name': self.street.neighborhood.city.state.name, 
            'j_state_abbreviation': self.street.neighborhood.city.state.pk, 
            'j_city_name': self.street.neighborhood.city.name, 
            'j_neighborhood_name': self.street.neighborhood.name, 
            'j_number': self.number,
            'j_complement': self.complement,
            'j_zipcode': self.street.zipcode,
            'j_latitude': self.latitude,
            'j_longitude': self.longitude,
            'j_use_type': self.use_type,
        }

        super(PhysicalAddress, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s (%s %s)' % (unicode(self.street), self.number or "", self.complement or "")

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
    