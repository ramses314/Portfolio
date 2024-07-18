from django.contrib import admin
from django.utils.html import mark_safe

from .forms import CustomEventEditForm

from ..core.admin import CommonAdmin, ThumbAdminMixin
from . import models


@admin.register(models.Event)
class EventAdmin(CommonAdmin):

    form = CustomEventEditForm

    readonly_fields = ('ticket_quantity',)

    list_display = [
        'title',
        'content',
        'created',
        'modified',
        'expired',
        'status',
        'ticket_quantity',
        'category',
        'link',
        'thumb_image',
    ]

    list_filter = [
        'status',
        'created',
        'expired',
        'category',
    ]

    search_fields = [
        'title',
        'content',
    ]

    ordering = [
        'status',
        'created',
    ]

    prepopulated_fields = {
        'slug': ['title'],
    }

    @admin.display(description='Image preview')
    def thumb_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100">')


@admin.register(models.Category)
class CategoryAdmin(CommonAdmin):
    list_display = [
        'title',
        'status',
        'created',
    ]

    search_fields = [
        'title',
    ]


@admin.register(models.Prize)
class PrizeAdmin(CommonAdmin):
    list_display = [
        'title',
        'content',
    ]

    search_fields = [
        'title',
        'content',
    ]


@admin.register(models.Ticket)
class TicketAdmin(
        ThumbAdminMixin,
        admin.ModelAdmin,
):
    list_display = [
        'event',
        'number',
        'price',
        'thumb_qr_code',
        'status',
    ]

    list_filter = [
        'status',
        'event',
    ]

    ordering = [
        'status',
    ]

    readonly_fields = [
        'uuid',
    ]

    image_list = [
        'qr_code',
    ]


@admin.register(models.Client)
class ClientAdmin(CommonAdmin):
    list_display = [
        'request_id',
        'status',
        'created',
    ]

    def has_module_permission(self, request):
        if request.user.groups.filter(name='admin').exists():
            return False
        return super().has_module_permission(request)

