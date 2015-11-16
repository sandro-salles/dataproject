# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from core.models import DatableModel, DirtyModel
from core.util import normalize_text, as_digits
from db.models.manager import UpsertManager


class Person(DatableModel, DirtyModel):

    NATURE_CHOICES_PHYSICAL = ('P', _(u'Física'))
    NATURE_CHOICES_LEGAL = ('L', _(u'Jurídica'))
    NATURE_CHOICES = (NATURE_CHOICES_PHYSICAL, NATURE_CHOICES_LEGAL)

    name = models.CharField(_('Nome'), db_index=True, max_length=300)
    nature = models.CharField(
        _('Natureza'), db_index=True, max_length=3, choices=NATURE_CHOICES)
    document = models.CharField(_(u'Documento'), max_length=14, unique=True)

    objects = UpsertManager()

    @property
    def unique_composition(self):
        return self.document

    class Meta:
        verbose_name = _("Pessoa")
        verbose_name_plural = _("Pessoas")

    def save(self, *args, **kwargs):
        self.document = as_digits(self.document)
        self.name = normalize_text(self.name)
        super(Person, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

