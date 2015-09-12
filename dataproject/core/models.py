# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings
from core.util import replace_diacritics
from django.utils.text import slugify


class SlugModel(models.Model):
    name = models.CharField(_('Nome'), max_length=200, null=False, blank=False)
    slug = models.SlugField(_('Identificador'), max_length=200, unique=True, null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(replace_diacritics(self.name))
        super(SlugModel, self).save(*args, **kwargs)


class DatableModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Corporation(SlugModel, DatableModel):

    class Meta:
        verbose_name = _('Empresa')
        verbose_name_plural = _('Empresas')

    def __unicode__(self):
        return self.name