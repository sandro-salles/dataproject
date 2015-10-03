# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from core.models import DatableModel, DirtyModel
from person.models import PhysicalPerson, LegalPerson
import reversion

@reversion.register
class CPF(DatableModel, DirtyModel):
    number = models.CharField(_(u'Número'), max_length=11, unique=True, db_index=True)
    person = models.ForeignKey(PhysicalPerson)

    class Meta:
        verbose_name        = _("CPF")
        verbose_name_plural = _("CPF's")

    def __unicode__(self):
        return self.number

@reversion.register
class RG(DatableModel, DirtyModel):    
    number = models.CharField(_(u'Número'), max_length=20, unique=True, db_index=True)
    person = models.ForeignKey(PhysicalPerson)
    issuer = models.CharField(_(u'Órgão Emissor'), max_length=300)

    class Meta:
        verbose_name        = _("RG")
        verbose_name_plural = _("RG's")

    def __unicode__(self):
        return self.number

@reversion.register
class CNPJ(DatableModel, DirtyModel):
    number = models.CharField(_(u'Número'), max_length=14, unique=True, db_index=True)
    person = models.ForeignKey(LegalPerson)

    class Meta:
        verbose_name        = _("CNPJ")
        verbose_name_plural = _("CNPJ's")

    def __unicode__(self):
        return self.number