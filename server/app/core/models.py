# -*- coding: utf-8 -*-

from django.db import models
from core.util import replace_diacritics
from django.utils.text import slugify


class SluggableModel(models.Model):
    name = models.CharField('Nome', max_length=200,
                            db_index=True, null=False, blank=False)
    slug = models.SlugField('Identificador', db_index=True,
                            max_length=200, unique=True, null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(replace_diacritics(self.name))
        super(SluggableModel, self).save(*args, **kwargs)


class DatableModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

class DirtyModel(models.Model):
    is_dirty = models.BooleanField('Inconsistente', default=False)

    class Meta:
        abstract = True
