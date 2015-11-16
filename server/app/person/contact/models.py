# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from core.models import DatableModel, SlugModel
from core.util import normalize_text
from person.models import Person
from localflavor.br.br_states import STATE_CHOICES
from db.models.manager import UpsertManager


class Carrier(SlugModel, DatableModel):

    verbose_name = _("Operadora de Telefonia")
    verbose_name_plural = _("Operadoras de Telefonia")

    def __unicode__(self):
        return self.name


class Contact(DatableModel):
    objects = UpsertManager()

    class Meta:
        abstract = True


class Address(Contact):

    persons = models.ManyToManyField(
        Person, through="PersonAddress", related_name='addresses')
    state = models.CharField(_(u'State'), max_length=2,
                             db_index=True, choices=STATE_CHOICES)
    city = models.CharField(_(u'Cidade'), max_length=200, db_index=True)
    neighborhood = models.CharField(_(u'Bairro'), max_length=200)
    location = models.TextField(_(u'Endereço'))
    zipcode = models.CharField(_(u'CEP'), max_length=8)

    class Meta:
        verbose_name = _(u"Endereço Físico")
        verbose_name_plural = _(u"Endereços Físicos")
        unique_together = ('zipcode', 'location')

    @property
    def unique_composition(self):
        return '%s_%s' % (self.zipcode, self.location)

    def save(self, *args, **kwargs):
        self.state = normalize_text(self.state)
        self.city = normalize_text(self.city)
        self.neighborhood = normalize_text(self.neighborhood)
        self.location = normalize_text(self.location)
        self.zipcode = normalize_text(self.zipcode)
        super(Address, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.location


class PersonAddress(DatableModel):
    person = models.ForeignKey(Person)
    address = models.ForeignKey(Address)

    objects = UpsertManager()

    @property
    def unique_composition(self):
        return '%s_%s' % (self.person.unique_composition, self.address.unique_composition)

    class Meta:
        unique_together = ('person', 'address')


class Phone(Contact):

    persons = models.ManyToManyField(
        Person, through="PersonPhone", related_name='phones')

    TYPE_CHOICES_CELLPHONE = ('cel', _('Celular'))
    TYPE_CHOICES_TELEPHONE = ('tel', _('Telefone Fixo'))
    TYPE_CHOICES = (TYPE_CHOICES_CELLPHONE, TYPE_CHOICES_TELEPHONE)

    type = models.CharField(_('Tipo do Aparelho'),
                            max_length=3, db_index=True, choices=TYPE_CHOICES)

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
        _(u' Código DDD'), db_index=True, choices=AREACODE_CHOICES)
    number = models.CharField(_(u'Número'), max_length=9)
    carrier = models.ForeignKey(Carrier)
    address = models.ForeignKey(Address)

    @property
    def unique_composition(self):
        return '%s_%s_%s' % (self.type, self.areacode, self.number)

    class Meta:
        verbose_name = _(u"Telefone")
        verbose_name_plural = _(u"Telefones")
        unique_together = ('type', 'areacode', 'number')

    def __unicode__(self):
        return '%s %s (%s)' % (self.areacode, self.number, self.type)


class PersonPhone(models.Model):
    person = models.ForeignKey(Person)
    phone = models.ForeignKey(Phone)

    objects = UpsertManager()

    @property
    def unique_composition(self):
        return '%s_%s' % (self.person.unique_composition, self.phone.unique_composition)

    class Meta:
        unique_together = ('person', 'phone')


class Email(Contact):

    persons = models.ManyToManyField(Person, through="PersonEmail")
    address = models.EmailField(_('E-mail'), unique=True)

    class Meta:
        verbose_name = _(u"Endereço Eletrônico")
        verbose_name_plural = _(u"Endereços Eletrônicos")


class PersonEmail(DatableModel):
    person = models.ForeignKey(Person)
    email = models.ForeignKey(Email)

    class Meta:
        unique_together = ('person', 'email')
