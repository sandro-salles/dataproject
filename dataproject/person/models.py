# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings
from polymorphic import PolymorphicModel
from core.models import SlugModel, DatableModel
from django_hstore import hstore
from core.util import sanitize_text

import reversion


class Person(PolymorphicModel, DatableModel):
    name = models.CharField(_('Nome'), max_length=300)

    json = hstore.DictionaryField(schema=[
        {
            'name': 'j_name',
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
        self.name = sanitize_text(self.name)
        self.json = {'j_name': self.name}
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