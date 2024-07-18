import uuid

from django.db import models

from ..core.models import Single


class Preference(Single):
    """
    Preference
    """

    front_uuid = models.UUIDField(
        verbose_name='FRONT_KEY',
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )

    site_title = models.CharField(
        verbose_name='Site title',
        max_length=200,
        blank=True,
    )

    google_redirect_url = models.CharField(
        verbose_name='Google url',
        max_length=255,
        blank=True,
    )

    front_url = models.CharField(
        verbose_name='Front URL',
        max_length=255,
        blank=True,
    )

    class Meta:
        verbose_name = 'settings: back'
        verbose_name_plural = 'settings: back'

    def __str__(self):
        return 'settings: back'


class TestBlock(Single):
    """
    Manage off/on some elements of project (for development)
    """

    order_expired = models.BooleanField(
        verbose_name='Order expired',
        default=True,
    )

    class Meta:
        verbose_name = 'Testing block'
        verbose_name_plural = 'Testing block'

    def __str__(self):
        return 'Testing block'
