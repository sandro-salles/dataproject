# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings
from polymorphic import PolymorphicModel
from core.models import DatableModel


class Person(PolymorphicModel, DatableModel):
    name = models.CharField(_('Nome'), max_length=300)

    class Meta:
        verbose_name        = _("Pessoa")
        verbose_name_plural = _("Pessoas")

    def __unicode__(self):
        return self.name


class Person(PolymorphicModel, DatableModel):
    name = models.CharField(_('Nome'), max_length=300)

    class Meta:
        verbose_name        = _("Pessoa")
        verbose_name_plural = _("Pessoas")

    def __unicode__(self):
        return self.name


class PhysicalPerson(Person):

    class Meta:
        verbose_name        = _(u"Pessoa Física")
        verbose_name_plural = _(u"Pessoas Físicas")


class LegalPerson(Person):

    class Meta:
        verbose_name        = _(u"Pessoa Jurídica")
        verbose_name_plural = _(u"Pessoas Jurídicas")