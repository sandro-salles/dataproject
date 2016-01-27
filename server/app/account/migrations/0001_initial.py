# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import authentication.models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '__first__'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'Nome', db_index=True)),
                ('slug', models.SlugField(null=True, max_length=200, blank=True, unique=True, verbose_name=b'Identificador')),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Conta',
                'verbose_name_plural': 'Contas',
            },
        ),
        migrations.CreateModel(
            name='Corporation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'Nome', db_index=True)),
                ('slug', models.SlugField(null=True, max_length=200, blank=True, unique=True, verbose_name=b'Identificador')),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('image', models.CharField(max_length=255, null=True, blank=True)),
                ('document', models.CharField(max_length=14)),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'Nome', db_index=True)),
                ('slug', models.SlugField(null=True, max_length=200, blank=True, unique=True, verbose_name=b'Identificador')),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('description', models.TextField(unique=True, max_length=14, verbose_name='Descricao')),
            ],
            options={
                'verbose_name': 'Funcionalidade',
                'verbose_name_plural': 'Funcionalidades',
            },
        ),
        migrations.CreateModel(
            name='Ownership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Propriedade de conta',
                'verbose_name_plural': 'Propriedades de contas',
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'Nome', db_index=True)),
                ('slug', models.SlugField(null=True, max_length=200, blank=True, unique=True, verbose_name=b'Identificador')),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('description', models.TextField(unique=True, max_length=14, verbose_name='Descricao')),
            ],
            options={
                'verbose_name': 'Plano',
                'verbose_name_plural': 'Planos',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Inscri\xe7\xe3o',
                'verbose_name_plural': 'Inscri\xe7\xf5es',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('deleted_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'Usu\xe1rio',
                'verbose_name_plural': 'Usu\xe1rios',
            },
            bases=('authentication.user', models.Model),
            managers=[
                ('objects', authentication.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Brass',
            fields=[
                ('plan_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='account.Plan')),
            ],
            options={
                'verbose_name': 'Plano Bronze',
                'verbose_name_plural': 'Planos Bronze',
            },
            bases=('account.plan',),
        ),
        migrations.CreateModel(
            name='CorporateAccount',
            fields=[
                ('account_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='account.Account')),
            ],
            options={
                'verbose_name': 'Conta Empresarial',
                'verbose_name_plural': 'Contas Empresariais',
            },
            bases=('account.account',),
        ),
        migrations.CreateModel(
            name='Diamond',
            fields=[
                ('plan_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='account.Plan')),
            ],
            options={
                'verbose_name': 'Plano Diamante',
                'verbose_name_plural': 'Planos Diamante',
            },
            bases=('account.plan',),
        ),
        migrations.CreateModel(
            name='Gold',
            fields=[
                ('plan_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='account.Plan')),
            ],
            options={
                'verbose_name': 'Plano Ouro',
                'verbose_name_plural': 'Planos Ouro',
            },
            bases=('account.plan',),
        ),
        migrations.CreateModel(
            name='PersonalAccount',
            fields=[
                ('account_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='account.Account')),
            ],
            options={
                'verbose_name': 'Conta Pessoal',
                'verbose_name_plural': 'Contas Pessoais',
            },
            bases=('account.account',),
        ),
        migrations.CreateModel(
            name='Silver',
            fields=[
                ('plan_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='account.Plan')),
            ],
            options={
                'verbose_name': 'Plano Prata',
                'verbose_name_plural': 'Planos Prata',
            },
            bases=('account.plan',),
        ),
        migrations.AddField(
            model_name='user',
            name='account',
            field=models.ForeignKey(related_name='users', to='account.Account'),
        ),
        migrations.AddField(
            model_name='user',
            name='created_by',
            field=models.ForeignKey(related_name='created_user', default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='deleted_by',
            field=models.ForeignKey(related_name='deleted_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_user', default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subscription',
            name='account',
            field=models.OneToOneField(related_name='subscription', to='account.Account'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='created_by',
            field=models.ForeignKey(related_name='created_subscription', default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subscription',
            name='deleted_by',
            field=models.ForeignKey(related_name='deleted_subscription', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='plan',
            field=models.ForeignKey(to='account.Plan'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_subscription', default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='plan',
            name='features',
            field=models.ManyToManyField(to='account.Feature'),
        ),
        migrations.AddField(
            model_name='plan',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_account.plan_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='ownership',
            name='account',
            field=models.OneToOneField(related_name='ownership', to='account.Account'),
        ),
        migrations.AddField(
            model_name='ownership',
            name='created_by',
            field=models.ForeignKey(related_name='created_ownership', default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ownership',
            name='deleted_by',
            field=models.ForeignKey(related_name='deleted_ownership', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='ownership',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_ownership', default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ownership',
            name='user',
            field=models.ForeignKey(related_name='ownerships', to='account.User'),
        ),
        migrations.AddField(
            model_name='corporation',
            name='created_by',
            field=models.ForeignKey(related_name='created_corporation', default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='corporation',
            name='deleted_by',
            field=models.ForeignKey(related_name='deleted_corporation', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='corporation',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_corporation', default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='account',
            name='created_by',
            field=models.ForeignKey(related_name='created_account', default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='account',
            name='deleted_by',
            field=models.ForeignKey(related_name='deleted_account', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_account.account_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='updated_by',
            field=models.ForeignKey(related_name='updated_account', default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='corporation',
            name='account',
            field=models.OneToOneField(related_name='corporation', to='account.CorporateAccount'),
        ),
    ]
