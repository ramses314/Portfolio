from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp
from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy
from singlemodeladmin import SingleModelAdmin

from . import models


@admin.register(models.Preference)
class PreferenceAdmin(SingleModelAdmin):
    readonly_fields = [
        'front_uuid',
    ]

    def has_module_permission(self, request):
        if request.user.groups.filter(name='admin').exists():
            return False
        return super().has_module_permission(request)


@admin.register(models.TestBlock)
class PreferenceAdmin(SingleModelAdmin):
    list_display = [
        'order_expired',
    ]

    def has_module_permission(self, request):
        if request.user.groups.filter(name='admin').exists():
            return False
        return super().has_module_permission(request)


admin.site.unregister(Group)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialApp)
admin.site.unregister(EmailAddress)
admin.site.unregister(TokenProxy)
