# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings
from polymorphic import PolymorphicModel
from core.models import SlugModel, DatableModel, DirtyModel
from django_hstore import hstore
from core.util import normalize_text, remove_spaces_and_similar

import reversion


class Person(PolymorphicModel, DatableModel, DirtyModel):
    name = models.CharField(_('Nome'), max_length=300)
    normal_name = models.CharField(_('Nome Normalizado'), max_length=300, db_index=True, editable=False)

    json = hstore.DictionaryField(schema=[
        {
            'name': 'j_name',
            'class': 'CharField',
            'kwargs': {
                'blank': False,
                'max_length': 300,
            }
        },
        {
            'name': 'j_normal_name',
            'class': 'CharField',
            'kwargs': {
                'blank': False,
                'max_length': 300,
            }
        }
    ], editable=False)

    objects = hstore.HStoreManager()

    class Meta:
        verbose_name        = _("Pessoa")
        verbose_name_plural = _("Pessoas")

    def save(self, *args, **kwargs):
        self.name = remove_spaces_and_similar(self.name)
        self.normal_name = normalize_text(self.name)
        self.json = {'j_name': self.name, 'j_normal_name': self.normal_name}
        super(Person, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

@reversion.register
class PhysicalPerson(Person):

    class Meta:
        verbose_name        = _(u"Pessoa Física")
        verbose_name_plural = _(u"Pessoas Físicas")

@reversion.register
class LegalPerson(Person):

    class Meta:
        verbose_name        = _(u"Pessoa Jurídica")
        verbose_name_plural = _(u"Pessoas Jurídicas")