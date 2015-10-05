# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from polymorphic import PolymorphicModel
from core.models import DatableModel, SlugModel, DirtyModel
from person.models import Person
from geo.models import Street, Neighborhood, City, State
from core.util import remove_spaces_and_similar
import mmh3
import reversion
from memoize import memoize


class Carrier(SlugModel, DatableModel):

    class Meta:
        verbose_name        = _("Operadora de Telefonia")
        verbose_name_plural = _("Operadoras de Telefonia")

    def __unicode__(self):
        return self.name





@reversion.register
class Phone(DatableModel):

    persons = models.ManyToManyField(Person, through="PersonPhone")

    TYPE_CHOICES_CELLPHONE  = ('cel', _('Celular'))
    TYPE_CHOICES_TELEPHONE  = ('tel', _('Telefone Fixo'))
    TYPE_CHOICES = (TYPE_CHOICES_CELLPHONE, TYPE_CHOICES_TELEPHONE)

    type = models.CharField(_('Tipo do Aparelho'), max_length=3, choices=TYPE_CHOICES)

    area_code = models.CharField(_('DDD'), max_length=2)
    number = models.CharField(_(u'Número'), max_length=9)
    carrier = models.ForeignKey(Carrier)
    hash = models.IntegerField(_('Hash'), unique=True, editable=False)

    class Meta:
        verbose_name        = _(u"Telefone")
        verbose_name_plural = _(u"Telefones")        
        unique_together     = ('type', 'area_code', 'number')

    
    @staticmethod
    @memoize()
    def make_hash(type, area_code, number):
        return mmh3.hash('%s%s%s' % (type, area_code, number))

    def save(self, *args, **kwargs):
        self.hash = Phone.make_hash(self.type, self.area_code, self.number)
        super(Phone, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s %s (%s)' % (self.area_code, self.number, self.type)


class PersonPhone(DatableModel):
    person = models.ForeignKey(Person)
    phone = models.ForeignKey(Phone)



class Address(DatableModel):

    persons = models.ManyToManyField(Person, through="PersonAddress")

    state = models.ForeignKey(State)
    city = models.ForeignKey(City)
    neighborhood = models.ForeignKey(Neighborhood)
    street = models.ForeignKey(Street)
    number = models.CharField(_(u'Número'), max_length=20, blank=True, null=True)
    complement = models.CharField(_(u'Complemento'), max_length=50, blank=True, null=True)
    
    hash = models.IntegerField(_('Hash'), unique=True, editable=False)

    class Meta:
        verbose_name        = _(u"Endereço Físico")
        verbose_name_plural = _(u"Endereços Físicos")
        unique_together     = ('street', 'number', 'complement')

    
    @staticmethod
    @memoize()
    def make_hash(zipcode, number, complement):
        return mmh3.hash('%s%s%s' % (zipcode, number, complement))

    def save(self, *args, **kwargs):
        self.number = remove_spaces_and_similar(self.number)
        self.complement = remove_spaces_and_similar(self.complement)
        self.hash = Phone.make_hash(self.street.zipcode, self.number, self.complement)
        super(Address, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s (%s %s)' % (unicode(self.street), self.number or "", self.complement or "")

class PersonAddress(DatableModel):
    person = models.ForeignKey(Person)
    address = models.ForeignKey(Address)

    
@reversion.register
class Email(DatableModel):

    persons = models.ManyToManyField(Person, through="PersonEmail")

    address = models.EmailField(_('E-mail'))

    class Meta:
        verbose_name        = _(u"Endereço Eletrônico")
        verbose_name_plural = _(u"Endereços Eletrônicos")

class PersonEmail(DatableModel):
    person = models.ForeignKey(Person)
    email = models.ForeignKey(Email)
    