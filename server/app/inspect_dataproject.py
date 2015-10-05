# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


class ContactCellphone(models.Model):
    phone_ptr = models.ForeignKey('ContactPhone', primary_key=True)
    use_type = models.CharField(max_length=50, blank=True, null=True)
    operator = models.ForeignKey('ContactMobileoperator')

    class Meta:
        managed = False
        db_table = 'contact_cellphone'


class ContactContact(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    polymorphic_ctype = models.ForeignKey('DjangoContentType', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_contact'


class ContactContactPersons(models.Model):
    contact = models.ForeignKey(ContactContact)
    person = models.ForeignKey('PersonPerson')

    class Meta:
        managed = False
        db_table = 'contact_contact_persons'
        unique_together = (('contact_id', 'person_id'),)


class ContactEmail(models.Model):
    contact_ptr = models.ForeignKey(ContactContact, primary_key=True)
    address = models.CharField(max_length=254)
    use_type = models.CharField(max_length=50, blank=True, null=True)
    json = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'contact_email'


class ContactMobileoperator(models.Model):
    phoneoperator_ptr = models.ForeignKey('ContactPhoneoperator', primary_key=True)

    class Meta:
        managed = False
        db_table = 'contact_mobileoperator'


class ContactPhone(models.Model):
    contact_ptr = models.ForeignKey(ContactContact, primary_key=True)
    country_code = models.CharField(max_length=3)
    area_code = models.CharField(max_length=2)
    number = models.CharField(max_length=9)
    json = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'contact_phone'
        unique_together = (('country_code', 'area_code', 'number'), ('area_code', 'number'),)


class ContactPhoneoperator(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(unique=True, max_length=200, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    polymorphic_ctype = models.ForeignKey('DjangoContentType', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_phoneoperator'


class ContactPhysicaladdress(models.Model):
    contact_ptr = models.ForeignKey(ContactContact, primary_key=True)
    address = models.TextField()
    zipcode = models.CharField(max_length=8)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    use_type = models.CharField(max_length=50, blank=True, null=True)
    json = models.TextField(blank=True, null=True)  # This field type is a guess.
    city = models.ForeignKey('GeoCity')
    neighborhood = models.ForeignKey('GeoNeighborhood')
    state = models.ForeignKey('GeoState')
    normal_address = models.TextField()

    class Meta:
        managed = False
        db_table = 'contact_address'


class ContactTelephone(models.Model):
    phone_ptr = models.ForeignKey(ContactPhone, primary_key=True)
    use_type = models.CharField(max_length=50, blank=True, null=True)
    operator = models.ForeignKey('ContactTelephoneoperator')

    class Meta:
        managed = False
        db_table = 'contact_telephone'


class ContactTelephoneoperator(models.Model):
    phoneoperator_ptr = models.ForeignKey(ContactPhoneoperator, primary_key=True)

    class Meta:
        managed = False
        db_table = 'contact_telephoneoperator'


class CoreCorporation(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(unique=True, max_length=200, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'core_corporation'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DocumentCnpj(models.Model):
    legalpersondocument_ptr = models.ForeignKey('DocumentLegalpersondocument', primary_key=True)

    class Meta:
        managed = False
        db_table = 'document_cnpj'


class DocumentCpf(models.Model):
    physicalpersondocument_ptr = models.ForeignKey('DocumentPhysicalpersondocument', primary_key=True)

    class Meta:
        managed = False
        db_table = 'document_cpf'


class DocumentLegalpersondocument(models.Model):
    persondocument_ptr = models.ForeignKey('DocumentPersondocument', primary_key=True)
    person = models.ForeignKey('PersonLegalperson')

    class Meta:
        managed = False
        db_table = 'document_legalpersondocument'


class DocumentPersondocument(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    number = models.CharField(max_length=20)
    polymorphic_ctype = models.ForeignKey(DjangoContentType, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'document_persondocument'


class DocumentPhysicalpersondocument(models.Model):
    persondocument_ptr = models.ForeignKey(DocumentPersondocument, primary_key=True)
    person = models.ForeignKey('PersonPhysicalperson')

    class Meta:
        managed = False
        db_table = 'document_physicalpersondocument'


class DocumentRg(models.Model):
    physicalpersondocument_ptr = models.ForeignKey(DocumentPhysicalpersondocument, primary_key=True)
    issuer = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'document_rg'


class GeoCity(models.Model):
    name = models.CharField(max_length=600)
    json = models.TextField(blank=True, null=True)  # This field type is a guess.
    state = models.ForeignKey('GeoState')

    class Meta:
        managed = False
        db_table = 'geo_city'


class GeoNeighborhood(models.Model):
    name = models.CharField(max_length=600)
    json = models.TextField(blank=True, null=True)  # This field type is a guess.
    city = models.ForeignKey(GeoCity)

    class Meta:
        managed = False
        db_table = 'geo_neighborhood'


class GeoState(models.Model):
    name = models.CharField(max_length=300)
    abbreviation = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'geo_state'


class LogBairro(models.Model):
    bai_nu_sequencial = models.IntegerField(primary_key=True)
    ufe_sg = models.CharField(max_length=2)
    loc_nu_sequencial = models.ForeignKey('LogLocalidade', db_column='loc_nu_sequencial')
    bai_no = models.CharField(max_length=72)
    bai_no_abrev = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_bairro'


class LogControle(models.Model):
    versao = models.CharField(max_length=4, blank=True, null=True)
    data = models.DateTimeField(blank=True, null=True)
    compl1 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_controle'


class LogCpc(models.Model):
    cpc_nu_sequencial = models.IntegerField(primary_key=True)
    ufe_sg = models.CharField(max_length=2)
    loc_nu_sequencial = models.ForeignKey('LogLocalidade', db_column='loc_nu_sequencial')
    cep = models.CharField(max_length=16)
    cpc_no = models.CharField(max_length=96)
    cpc_endereco = models.CharField(max_length=108)
    cpc_tipo = models.CharField(max_length=2, blank=True, null=True)
    cpc_abrangencia = models.CharField(max_length=80, blank=True, null=True)
    temp = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_cpc'


class LogFaixaBairro(models.Model):
    bai_nu_sequencial = models.ForeignKey(LogBairro, db_column='bai_nu_sequencial')
    fcb_nu_ordem = models.IntegerField()
    fcb_rad_ini = models.CharField(max_length=5)
    fcb_suf_ini = models.CharField(max_length=3)
    fcb_rad_fim = models.CharField(max_length=5)
    fcb_suf_fim = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'log_faixa_bairro'
        unique_together = (('bai_nu_sequencial', 'fcb_nu_ordem'),)


class LogFaixaCpc(models.Model):
    cpc_nu_sequencial = models.ForeignKey(LogCpc, db_column='cpc_nu_sequencial')
    cpc_nu_inicial = models.IntegerField()
    cpc_nu_final = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'log_faixa_cpc'
        unique_together = (('cpc_nu_inicial', 'cpc_nu_sequencial'),)


class LogFaixaLocalidade(models.Model):
    loc_nu_sequencial = models.ForeignKey('LogLocalidade', db_column='loc_nu_sequencial', primary_key=True)
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


class LogFaixaUf(models.Model):
    ufe_sg = models.CharField(primary_key=True, max_length=2)
    ufe_no = models.CharField(max_length=72)
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


class LogFaixaUop(models.Model):
    uop_nu_sequencial = models.ForeignKey('LogUnidOper', db_column='uop_nu_sequencial')
    fnc_nu_inicial = models.IntegerField()
    fnc_nu_final = models.IntegerField(blank=True, null=True)
    fnc_in_tipo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_faixa_uop'
        unique_together = (('fnc_nu_inicial', 'uop_nu_sequencial'),)


class LogGrandeUsuario(models.Model):
    gru_nu_sequencial = models.IntegerField(primary_key=True)
    ufe_sg = models.CharField(max_length=2)
    loc_nu_sequencial = models.ForeignKey('LogLocalidade', db_column='loc_nu_sequencial')
    log_nu_sequencial = models.ForeignKey('LogLogradouro', db_column='log_nu_sequencial', blank=True, null=True)
    bai_nu_sequencial = models.ForeignKey(LogBairro, db_column='bai_nu_sequencial')
    gru_no = models.CharField(max_length=96)
    cep = models.CharField(max_length=16)
    gru_endereco = models.CharField(max_length=200)
    temp = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_grande_usuario'


class LogLocalidade(models.Model):
    loc_nu_sequencial = models.IntegerField(primary_key=True)
    loc_nosub = models.CharField(max_length=50, blank=True, null=True)
    loc_no = models.CharField(max_length=60, blank=True, null=True)
    cep = models.CharField(max_length=16, blank=True, null=True)
    ufe_sg = models.ForeignKey(LogFaixaUf, db_column='ufe_sg', blank=True, null=True)
    loc_in_situacao = models.IntegerField(blank=True, null=True)
    loc_in_tipo_localidade = models.CharField(max_length=1)
    loc_nu_sequencial_sub = models.IntegerField(blank=True, null=True)
    temp = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_localidade'


class LogLogradouro(models.Model):
    log_nu_sequencial = models.IntegerField(primary_key=True)
    ufe_sg = models.CharField(max_length=2)
    loc_nu_sequencial = models.ForeignKey(LogLocalidade, db_column='loc_nu_sequencial')
    log_no = models.CharField(max_length=70)
    log_nome = models.CharField(max_length=125)
    bai_nu_sequencial_ini = models.ForeignKey(LogBairro, db_column='bai_nu_sequencial_ini')
    bai_nu_sequencial_fim = models.IntegerField(blank=True, null=True)
    cep = models.CharField(max_length=16)
    log_complemento = models.CharField(max_length=100, blank=True, null=True)
    log_tipo_logradouro = models.CharField(max_length=72, blank=True, null=True)
    log_status_tipo_log = models.CharField(max_length=1)
    log_no_sem_acento = models.CharField(max_length=70)
    ind_uop = models.CharField(max_length=1, blank=True, null=True)
    ind_gru = models.CharField(max_length=1, blank=True, null=True)
    temp = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_logradouro'


class LogTipoLogr(models.Model):
    tipologradouro = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_tipo_logr'


class LogUnidOper(models.Model):
    uop_nu_sequencial = models.IntegerField(primary_key=True)
    ufe_sg = models.CharField(max_length=2)
    loc_nu_sequencial = models.ForeignKey(LogLocalidade, db_column='loc_nu_sequencial')
    log_nu_sequencial = models.ForeignKey(LogLogradouro, db_column='log_nu_sequencial', blank=True, null=True)
    bai_nu_sequencial = models.ForeignKey(LogBairro, db_column='bai_nu_sequencial')
    uop_no = models.CharField(max_length=100)
    cep = models.CharField(max_length=16)
    uop_endereco = models.CharField(max_length=200)
    uop_in_cp = models.CharField(max_length=1, blank=True, null=True)
    temp = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_unid_oper'


class PersonLegalperson(models.Model):
    person_ptr = models.ForeignKey('PersonPerson', primary_key=True)

    class Meta:
        managed = False
        db_table = 'person_legalperson'


class PersonPerson(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=300)
    json = models.TextField(blank=True, null=True)  # This field type is a guess.
    polymorphic_ctype = models.ForeignKey(DjangoContentType, blank=True, null=True)
    normal_name = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'person_person'


class PersonPhysicalperson(models.Model):
    person_ptr = models.ForeignKey(PersonPerson, primary_key=True)

    class Meta:
        managed = False
        db_table = 'person_physicalperson'


class ReversionRevision(models.Model):
    manager_slug = models.CharField(max_length=191)
    date_created = models.DateTimeField()
    comment = models.TextField()
    user = models.ForeignKey(AuthUser, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reversion_revision'


class ReversionVersion(models.Model):
    object_id = models.TextField()
    object_id_int = models.IntegerField(blank=True, null=True)
    format = models.CharField(max_length=255)
    serialized_data = models.TextField()
    object_repr = models.TextField()
    content_type = models.ForeignKey(DjangoContentType)
    revision = models.ForeignKey(ReversionRevision)

    class Meta:
        managed = False
        db_table = 'reversion_version'
