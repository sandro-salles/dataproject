# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from core.models import DatableModel, DirtyModel
from core.util import normalize_text
import reversion
from reversion.models import Revision
from memoize import memoize
import mmh3


@reversion.register
class Person(DatableModel, DirtyModel):

    NATURE_CHOICES_PHYSICAL = ('P', _(u'Física'))
    NATURE_CHOICES_LEGAL = ('L', _(u'Jurídica'))
    NATURE_CHOICES = (NATURE_CHOICES_PHYSICAL, NATURE_CHOICES_LEGAL)

    name = models.CharField(_('Nome'), db_index=True, max_length=300)
    nature = models.CharField(
        _('Natureza'), db_index=True, max_length=3, choices=NATURE_CHOICES)
    document = models.CharField(_(u'Documento'), max_length=30, unique=True)
    hash = models.IntegerField(_('Hash'), unique=True, editable=False)

    class Meta:
        verbose_name = _("Pessoa")
        verbose_name_plural = _("Pessoas")

    @staticmethod
    @memoize()
    def make_hash(document):
        return mmh3.hash('%s' % (document))

    def save(self, *args, **kwargs):
        self.hash = Person.make_hash(self.document)
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
