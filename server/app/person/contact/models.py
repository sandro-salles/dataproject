# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings
from core.models import DatableModel, SlugModel, DirtyModel
from person.models import Person
from geo.models import Street, Neighborhood, City, State
from core.util import remove_spaces_and_similar
import mmh3


class Carrier(SlugModel, DatableModel):

    class Meta:
        verbose_name        = _("Operadora de Telefonia")
        verbose_name_plural = _("Operadoras de Telefonia")

    def __unicode__(self):
        return self.name


class Contact(DatableModel, DirtyModel):
    persons = models.ManyToManyField(Person, through='PersonContact')
        
    class Meta:
        abstract = True


class PersonContact(models.Model):
    person = models.ForeignKey(Person)
    contact = models.ForeignKey(Contact)

    USE_TYPE_CHOICES_HOME       = ('res', _('Residencial'))
    USE_TYPE_CHOICES_COMMERCIAL = ('com', _('Comercial'))
    USE_TYPE_CHOICES_MESSAGES   = ('rec', _('Recados'))
    USE_TYPE_CHOICES_PERSONAL   = ('pes', _('Pessoal'))
    USE_TYPE_CHOICES_CORPORATE  = ('cor', _('Corporativo'))

    USE_TYPE_CHOICES            = (USE_TYPE_CHOICES_HOME, USE_TYPE_CHOICES_COMMERCIAL, USE_TYPE_CHOICES_MESSAGES, USE_TYPE_CHOICES_PERSONAL, USE_TYPE_CHOICES_CORPORATE)

    use_type = models.CharField(_('Tipo de Uso'), db_index=True, max_length=50, choices=USE_TYPE_CHOICES, blank=True, null=True)


class Phone(Contact):


    COUNTRY_CODE_CHOICES_BRAZIL = ('+55', _('Brasil'))
    COUNTRY_CODE_CHOICES = (COUNTRY_CODE_CHOICES_BRAZIL, )

    country_code = models.CharField(_('DDI'), max_length=3, choices=COUNTRY_CODE_CHOICES, default=COUNTRY_CODE_CHOICES_BRAZIL[0], db_index=True)

    TYPE_CHOICES_CELLPHONE  = ('cel', _('Celular'))
    TYPE_CHOICES_TELEPHONE  = ('tel', _('Telefone Fixo'))
    TYPE_CHOICES = (TYPE_CHOICES_CELLPHONE, TYPE_CHOICES_TELEPHONE)

    type = models.CharField(_('Tipo do Aparelho'), max_length=3, choices=TYPE_CHOICES, db_index=True)

    area_code = models.CharField(_('DDD'), max_length=2, db_index=True)
    number = models.CharField(_(u'Número'), max_length=9, db_index=True)
    carrier = models.ForeignKey(Carrier)
    hash = models.IntegerField(_('Hash'), unique=True, db_index=True, editable=False)

    class Meta:
        verbose_name        = _(u"Telefone")
        verbose_name_plural = _(u"Telefones")        
        unique_together     = ('country_code', 'area_code', 'number')

    @staticmethod
    def make_hash(country_code, area_code, number):
        return mmh3.hash('%s%s%s' % (country_code, area_code, number))

    def save(self, *args, **kwargs):
        self.hash = Phone.make_hash(self.country_code, self.area_code, self.number)
        super(Phone, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s %s %s (%s)' % (self.country_code, self.area_code, self.number, self.type)



class PhysicalAddress(Contact):

    state = models.ForeignKey(State)
    city = models.ForeignKey(City)
    neighborhood = models.ForeignKey(Neighborhood)
    street = models.ForeignKey(Street)
    number = models.CharField(_(u'Número'), db_index=True, max_length=20, blank=True, null=True)
    complement = models.CharField(_(u'Complemento'), db_index=True, max_length=50, blank=True, null=True)
    
    latitude = models.FloatField(_('Latitude'), db_index=True, blank=True, null=True)
    longitude = models.FloatField(_('Longitude'), db_index=True, blank=True, null=True)

    hash = models.IntegerField(_('Hash'), unique=True, db_index=True, editable=False)

    class Meta:
        verbose_name        = _(u"Endereço Físico")
        verbose_name_plural = _(u"Endereços Físicos")
        unique_together     = ('street', 'number', 'complement')

    @staticmethod
    def make_hash(zipcode, number, complement):
        return mmh3.hash('%s%s%s' % (zipcode, number, complement))

    def save(self, *args, **kwargs):
        self.number = remove_spaces_and_similar(self.number)
        self.complement = remove_spaces_and_similar(self.complement)
        self.hash = Phone.make_hash(self.street.zipcode, self.number, self.complement)
        super(PhysicalAddress, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s (%s %s)' % (unicode(self.street), self.number or "", self.complement or "")


class Email(Contact):

    address = models.EmailField(_('E-mail'))

    class Meta:
        verbose_name        = _(u"Endereço Eletrônico")
        verbose_name_plural = _(u"Endereços Eletrônicos")
    