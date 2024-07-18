from django.contrib import admin
from django.shortcuts import redirect
from singlemodeladmin import SingleModelAdmin

from ..core.admin import CommonAdmin, ThumbAdminMixin
from ..events.models import Ticket
from . import models


class TicketInlineAdmin(
        ThumbAdminMixin,
        admin.TabularInline,
):
    model = Ticket
    extra = 0
    exclude = ['qr_code,']

    readonly_fields = [
        'thumb_qr_code',
    ]

    image_list = [
        'qr_code',
    ]


@admin.register(models.Order)
class OrderAdmin(CommonAdmin):

    def create_order_detail(self, request, queryset=None):
        return redirect('main:excel')

    create_order_detail.short_description = 'export excel'
    actions = [create_order_detail]

    list_display = [
        'name_or_session_uuid',
        'uuid',
        'phone',
        'status',
        'email',
        'admin_comment',
        'description',
        'ticket_count',
        'created',
    ]

    list_filter = [
        'status',
        'created',
        'email',
    ]

    search_fields = [
        'user_uuid',
    ]

    ordering = [
        'status',
        'created',
    ]

    readonly_fields = [
        'uuid',
        'user_uuid',
    ]

    inlines = [
        TicketInlineAdmin,
    ]

    @admin.display(description='sessionUUID or name — email')
    def name_or_session_uuid(self, obj):
        if obj.name:
            return f'{obj.name} — {obj.email}'
        return obj.user_uuid

    @admin.display(description='Tickets')
    def ticket_count(self, obj):
        return obj.tickets.count()


@admin.register(models.LetterImage)
class LetterImageAdmin(admin.ModelAdmin):
    list_display = [
        'title',
    ]

    def has_module_permission(self, request):
        if request.user.groups.filter(name='admin').exists():
            return False
        return super().has_module_permission(request)


@admin.register(models.MercadoPago)
class MercadoPagoAdmin(SingleModelAdmin):
    list_display = [
        'access_token',
    ]

    def has_module_permission(self, request):
        if request.user.groups.filter(name='admin').exists():
            return False
        return super().has_module_permission(request)
