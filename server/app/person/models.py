# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from core.models import DatableModel, DirtyModel
from core.util import normalize_text, as_digits
import reversion
from reversion.models import Revision
from db.models.manager import UpsertManager


@reversion.register
class Person(DatableModel, DirtyModel):

    NATURE_CHOICES_PHYSICAL = ('P', _(u'Física'))
    NATURE_CHOICES_LEGAL = ('L', _(u'Jurídica'))
    NATURE_CHOICES = (NATURE_CHOICES_PHYSICAL, NATURE_CHOICES_LEGAL)

    name = models.CharField(_('Nome'), db_index=True, max_length=300)
    nature = models.CharField(
        _('Natureza'), db_index=True, max_length=3, choices=NATURE_CHOICES)
    document = models.CharField(_(u'Documento'), max_length=14, unique=True)

    objects = UpsertManager()

    class Meta:
        verbose_name = _("Pessoa")
        verbose_name_plural = _("Pessoas")

    def save(self, *args, **kwargs):
        self.document = as_digits(self.document)
        self.name = normalize_text(self.name)
        super(Person, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Collection(DatableModel):
    name = models.CharField(_('Nome'), max_length=200, null=False, blank=False)
    persons = models.ManyToManyField(Person, through='CollectionItem')

    class Meta:
        verbose_name = _(u'Coleção de Pessoas')
        verbose_name_plural = _(u'Coleções de Pessoas')

    def __unicode__(self):
        return self.name


class CollectionItem(models.Model):
    person = models.ForeignKey(Person)
    collection = models.ForeignKey(Collection)
    revision = models.ForeignKey(Revision)

    class Meta:
        verbose_name = _(u"Item de Coleção de Pessoas")
        verbose_name_plural = _(u"Itens de Coleção de Pessoas")

    def __unicode__(self):
        return self.person
