# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from polymorphic import PolymorphicModel
from core.models import DatableModel, DirtyModel
from person.models import PhysicalPerson, LegalPerson

import reversion


class PersonDocument(PolymorphicModel, DatableModel, DirtyModel):
    number = models.CharField(_(u'Número'), max_length=20, db_index=True)

    class Meta:
        verbose_name        = _("Documento Pessoal")
        verbose_name_plural = _("Documentos Pessoais")

    def __unicode__(self):
        return self.id


class PhysicalPersonDocument(PersonDocument):
    person = models.ForeignKey(PhysicalPerson)
    unique_together = ('number', 'person')

    class Meta:
        verbose_name        = _(u"Documento de Pessoa Física")
        verbose_name_plural = _(u"Documentos de Pessoa Física")


class LegalPersonDocument(PersonDocument):
    person = models.ForeignKey(LegalPerson)
    unique_together = ('number', 'person')

    class Meta:
        verbose_name        = _(u"Documento de Pessoa Jurídica")
        verbose_name_plural = _(u"Documentos de Pessoa Jurídica")


@reversion.register
class CPF(PhysicalPersonDocument):

    class Meta:
        verbose_name        = _("CPF")
        verbose_name_plural = _("CPF's")

    def __unicode__(self):
        return self.number

@reversion.register
class RG(PhysicalPersonDocument):    
    issuer = models.CharField(_(u'Órgão Emissor'), max_length=300)

    class Meta:
        verbose_name        = _("RG")
        verbose_name_plural = _("RG's")

    def __unicode__(self):
        return self.number

@reversion.register
class CNPJ(LegalPersonDocument):

    class Meta:
        verbose_name        = _("CNPJ")
        verbose_name_plural = _("CNPJ's")

    def __unicode__(self):
        return self.number