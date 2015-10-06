# -*- coding: utf-8 -*-

from django.db import models


class State(models.Model):
    id = models.CharField(primary_key=True, max_length=2, db_column='ufe_sg')
    name = models.CharField(max_length=72, db_column='ufe_no')
    ufe_rad1_ini = models.CharField(max_length=5)
    ufe_suf1_ini = models.CharField(max_length=3)
    ufe_rad1_fim = models.CharField(max_length=5)
    ufe_suf1_fim = models.CharField(max_length=3)
    ufe_rad2_ini = models.CharField(max_length=5, blank=True, null=True)
    ufe_suf2_ini = models.CharField(max_length=3, blank=True, null=True)
    ufe_rad2_fim = models.CharField(max_length=5, blank=True, null=True)
    ufe_suf2_fim = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_faixa_uf'

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.id)


class City(models.Model):
    id = models.IntegerField(primary_key=True, db_column='loc_nu_sequencial')
    name = models.CharField(max_length=50, blank=True,
                            null=True, db_column='loc_nosub')
    zipcode = models.CharField(
        max_length=16, blank=True, null=True, db_column='cep')
    state = models.ForeignKey(State, db_column='ufe_sg', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_localidade'

    def __unicode__(self):
        return '%s - %s' % (self.name, self.state.id)


class CityZipRange(models.Model):
    city = models.ForeignKey(
        City, db_column='loc_nu_sequencial', primary_key=True)
    loc_rad1_ini = models.CharField(max_length=5)
    loc_suf1_ini = models.CharField(max_length=3)
    loc_rad1_fim = models.CharField(max_length=5)
    loc_suf1_fim = models.CharField(max_length=3)
    loc_rad2_ini = models.CharField(max_length=5, blank=True, null=True)
    loc_suf2_ini = models.CharField(max_length=3, blank=True, null=True)
    loc_rad2_fim = models.CharField(max_length=5, blank=True, null=True)
    loc_suf2_fim = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_faixa_localidade'


class Neighborhood(models.Model):
    id = models.IntegerField(primary_key=True, db_column='bai_nu_sequencial')
    city = models.ForeignKey(City, db_column='loc_nu_sequencial')
    name = models.CharField(max_length=72, db_column='bai_no')
    abbreviation = models.CharField(
        max_length=36, blank=True, null=True, db_column='bai_no_abrev')

    class Meta:
        managed = False
        db_table = 'log_bairro'

    def __unicode__(self):
        return '%s - %s' % (self.name, self.city)


class NeighborhoodZipRange(models.Model):
    neighborhood = models.ForeignKey(
        Neighborhood, db_column='bai_nu_sequencial')
    fcb_nu_ordem = models.IntegerField()
    fcb_rad_ini = models.CharField(max_length=5)
    fcb_suf_ini = models.CharField(max_length=3)
    fcb_rad_fim = models.CharField(max_length=5)
    fcb_suf_fim = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'log_faixa_bairro'
        unique_together = (('neighborhood', 'fcb_nu_ordem'),)


class Street(models.Model):
    id = models.IntegerField(primary_key=True, db_column='log_nu_sequencial')
    city = models.ForeignKey(City, db_column='loc_nu_sequencial')
    name = models.CharField(max_length=70, db_column='log_no')
    neighborhood = models.ForeignKey(
        Neighborhood, db_column='bai_nu_sequencial_ini')
    zipcode = models.CharField(max_length=16, db_column='cep', db_index=True)
    type = models.CharField(max_length=72, blank=True,
                            null=True, db_column='log_tipo_logradouro')
    normalized_name = models.CharField(
        max_length=70, db_column='log_no_sem_acento')

    class Meta:
        managed = False
        db_table = 'log_logradouro'

    def __unicode__(self):
        return '%s %s - %s' % (self.type, self.name, self.neighborhood)
