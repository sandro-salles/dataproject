# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings
from polymorphic import PolymorphicModel
from core.models import SlugModel, DatableModel, DirtyModel
from core.util import normalize_text, remove_spaces_and_similar
import reversion
from reversion.models import Revision


@reversion.register
class Person(PolymorphicModel, DatableModel, DirtyModel):
    name = models.CharField(_('Nome'), db_index=True, max_length=300)

    class Meta:
        verbose_name        = _("Pessoa")
        verbose_name_plural = _("Pessoas")

    def save(self, *args, **kwargs):
        self.name = remove_spaces_and_similar(self.name)
        super(Person, self).save(*args, **kwargs)

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
        verbose_name        = _(u"Item de Coleção de Pessoas")
        verbose_name_plural = _(u"Itens de Coleção de Pessoas")

    def __unicode__(self):
        return self.person