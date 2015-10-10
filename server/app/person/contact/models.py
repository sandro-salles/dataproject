# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from core.models import DatableModel, SlugModel
from core.util import normalize_text
from person.models import Person
import mmh3
import reversion
from memoize import memoize
from localflavor.br.br_states import STATE_CHOICES


class Carrier(SlugModel, DatableModel):

    verbose_name = _("Operadora de Telefonia")
    verbose_name_plural = _("Operadoras de Telefonia")

    def __unicode__(self):
        return self.name


@reversion.register
class Phone(DatableModel):

    persons = models.ManyToManyField(Person, through="PersonPhone")

    TYPE_CHOICES_CELLPHONE = ('cel', _('Celular'))
    TYPE_CHOICES_TELEPHONE = ('tel', _('Telefone Fixo'))
    TYPE_CHOICES = (TYPE_CHOICES_CELLPHONE, TYPE_CHOICES_TELEPHONE)

    type = models.CharField(_('Tipo do Aparelho'),
                            max_length=3, choices=TYPE_CHOICES)

    AREACODE_CHOICES = ((11, 11), (12, 12), (13, 13), (14, 14), (15, 15),
                        (16, 16), (17, 17), (18, 18), (19, 19), (21, 21),
                        (22, 22), (24, 24), (27, 27), (28, 28), (31, 31),
                        (32, 32), (33, 33), (34, 34), (35, 35), (37, 37),
                        (38, 38), (41, 41), (42, 42), (43, 43), (44, 44),
                        (45, 45), (46, 46), (47, 47), (48, 48), (49, 49),
                        (51, 51), (53, 53), (54, 54), (55, 55), (61, 61),
                        (62, 62), (63, 63), (64, 64), (65, 65), (66, 66),
                        (67, 67), (68, 68), (69, 69), (71, 71), (73, 73),
                        (74, 74), (75, 75), (77, 77), (79, 79), (81, 81),
                        (82, 82), (83, 83), (84, 84), (85, 85), (86, 86),
                        (87, 87), (88, 88), (89, 89), (91, 91), (92, 92),
                        (93, 93), (94, 94), (95, 95), (96, 96), (97, 97),
                        (98, 98), (99, 99),)

    areacode = models.IntegerField(
        _(u' Código DDD'), choices=AREACODE_CHOICES)
    number = models.CharField(_(u'Número'), max_length=9)
    carrier = models.ForeignKey(Carrier)
    hash = models.IntegerField(_('Hash'), unique=True, editable=False)

    class Meta:
        verbose_name = _(u"Telefone")
        verbose_name_plural = _(u"Telefones")
        unique_together = ('type', 'areacode', 'number')

    @staticmethod
    @memoize()
    def make_hash(type, areacode, number):
        return mmh3.hash('%s%s%s' % (type, areacode, number))

    def save(self, *args, **kwargs):
        self.hash = Phone.make_hash(self.type, self.areacode, self.number)
        super(Phone, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s %s (%s)' % (self.areacode, self.number, self.type)


class PersonPhone(models.Model):
    person = models.ForeignKey(Person)
    phone = models.ForeignKey(Phone)


class Address(DatableModel):

    persons = models.ManyToManyField(Person, through="PersonAddress")
    state = models.CharField(_(u'State'), max_length=2, db_index=True, choices=STATE_CHOICES)
    city = models.CharField(_(u'Cidade'), max_length=200)
    neighborhood = models.CharField(_(u'Bairro'), max_length=200)
    location = models.TextField(_(u'Endereço'))
    zipcode = models.CharField(_(u'CEP'), max_length=8)
    hash = models.IntegerField(_('Hash'), unique=True, editable=False)

    class Meta:
        verbose_name = _(u"Endereço Físico")
        verbose_name_plural = _(u"Endereços Físicos")

    @staticmethod
    @memoize()
    def make_hash(zipcode, location):
        return mmh3.hash('%s%s' % (zipcode, location))

    def save(self, *args, **kwargs):
        self.location = normalize_text(self.location)
        self.hash = Phone.make_hash(self.zipcode, self.location)
        super(Address, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.location


class PersonAddress(DatableModel):
    person = models.ForeignKey(Person)
    address = models.ForeignKey(Address)


class Email(DatableModel):

    persons = models.ManyToManyField(Person, through="PersonEmail")
    address = models.EmailField(_('E-mail'))

    class Meta:
        verbose_name = _(u"Endereço Eletrônico")
        verbose_name_plural = _(u"Endereços Eletrônicos")


class PersonEmail(DatableModel):
    person = models.ForeignKey(Person)
    email = models.ForeignKey(Email)