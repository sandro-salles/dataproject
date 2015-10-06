# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from core.util import replace_diacritics
from django.utils.text import slugify


class SlugModel(models.Model):
    name = models.CharField(_('Nome'), max_length=200,
                            db_index=True, null=False, blank=False)
    slug = models.SlugField(_('Identificador'), db_index=True,
                            max_length=200, unique=True, null=True, blank=True)

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


class HashableModel(models.Model):
    hash = models.IntegerField(_('Hash'), editable=False)

    class Meta:
        abstract = True


class DirtyModel(models.Model):
    is_dirty = models.BooleanField(_('Inconsistente'), default=False)

    class Meta:
        abstract = True
