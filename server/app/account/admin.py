from django.contrib import admin
from account.models import *
from django.utils.six.moves.urllib.parse import (
    quote, quote_plus, unquote, unquote_plus, urlencode as original_urlencode,
    urlparse,
)

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm, UserCreationForm as DjangoUserCreationForm



class UserChangeForm(DjangoUserChangeForm):

    class Meta(DjangoUserChangeForm.Meta):
        model = User      


class UserCreateForm(DjangoUserCreationForm):

    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = ('username', 'account',)


class UserAdmin(DjangoUserAdmin):
    form = UserChangeForm
    add_form = UserCreateForm

    fieldsets = (
        (None, {'fields': ('account', )}),
    ) + DjangoUserAdmin.fieldsets
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('account', 'username', 'password1', 'password2'),
        }),
    )


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'type', 'created_at', 'updated_at')

    class Meta:
        model = Account

class CorporateAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')

    class Meta:
        model = CorporateAccount

class PersonalAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')

    class Meta:
        model = PersonalAccount


class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)

    class Meta:
        model = Plan


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('account', 'plan', 'created_at', 'updated_at')

    class Meta:
        model = Subscription


class CorporationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'account', 'created_at', 'updated_at')

    class Meta:
        model = Corporation


admin.site.register(User, UserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(PersonalAccount, PersonalAccountAdmin)
admin.site.register(CorporateAccount, CorporateAccountAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Corporation, CorporationAdmin)

