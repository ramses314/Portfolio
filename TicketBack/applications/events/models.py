import io
import uuid

import qrcode
from django.contrib.sites.models import Site
from django.core.files import File
from django.db import models

from applications.core.models import Common, PathAndRename
from applications.sales.models import Order


class Client(Common):

    request_id = models.CharField(
        max_length=255
    ) # yapf:disable


class Category(Common):
    '''
    Category event
    '''

    title = models.CharField(
        verbose_name='Title',
        max_length=255,
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title


class Event(Common):
    '''
    Event
    '''

    title = models.CharField(
        verbose_name='Title',
        max_length=200,
    )

    slug = models.CharField(
        verbose_name='Slug',
        max_length=200,
        unique=True,
        blank=True,
        null=True,
    )

    counter = models.IntegerField(
        verbose_name='counter',
        default=0,
    )

    price = models.DecimalField(
        verbose_name='Price',
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    on_landing = models.BooleanField(
        verbose_name='On Landing',
        default=False,
    )

    content = models.TextField(
        verbose_name='Content',
    )  # yapf: disable

    expired = models.DateTimeField(
        verbose_name='Expired',
    ) # yapf: disable

    image = models.ImageField(
        verbose_name='Image',
        upload_to=PathAndRename('events/event/image'),
        blank=True,
        null=True,
    )

    ticket_quantity = models.BigIntegerField(
        verbose_name='Ticket quantity',
        default=0,
    )

    category = models.ForeignKey(
        verbose_name='Category',
        to=Category,
        on_delete=models.CASCADE,
        related_name='events',
    )

    link = models.CharField(
        verbose_name='Translation link',
        max_length=500,
    )

    time_event = models.TimeField(
        verbose_name='Time to event',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'event'
        verbose_name_plural = 'events'

    def __str__(self):
        return self.title


class Prize(Common):
    '''
    Events prize
    '''

    title = models.CharField(
        verbose_name='Title',
        max_length=200,
    )

    content = models.TextField(
        verbose_name='Content',
    )  # yapf: disable

    image = models.ImageField(
        verbose_name='Image',
        upload_to=PathAndRename('events/prize/image'),
        blank=True,
        null=True,
    )

    event = models.ForeignKey(
        verbose_name='Event',
        to=Event,
        on_delete=models.CASCADE,
        related_name='prizes',
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'prize'
        verbose_name_plural = 'prizes'

    def __str__(self):
        return self.title


class Ticket(models.Model):
    '''
    Event ticket
    '''

    uuid = models.UUIDField(
        verbose_name='Unique id',
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )

    class Status(models.TextChoices):
        SOLD = 'sold', 'sold'
        BLOCKED = 'blocked', 'blocked'
        OPEN = 'open', 'open'

    status = models.CharField(
        verbose_name='Status',
        max_length=50,
        choices=Status.choices,
        default=Status.OPEN,
    )

    event = models.ForeignKey(
        verbose_name='Event',
        to=Event,
        on_delete=models.PROTECT,
        related_name='tickets',
    )

    number = models.BigIntegerField(
        verbose_name='Number',
    ) # yapf:disable

    price = models.DecimalField(
        verbose_name='Price',
        max_digits=10,
        decimal_places=2,
    )

    qr_code = models.ImageField(
        verbose_name='QR',
        upload_to=PathAndRename('events/ticket/qr_code'),
        blank=True,
        null=True,
    )

    order = models.ForeignKey(
        verbose_name='Order',
        to=Order,
        on_delete=models.SET_NULL,
        related_name='tickets',
        blank=True,
        null=True,
    )

    is_winner = models.BooleanField(
        verbose_name='Winner?',
        default=False,
    )

    prize_id = models.ForeignKey(
        verbose_name='prize_id',
        to=Prize,
        on_delete=models.CASCADE,
        related_name='prize',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'ticket'
        verbose_name_plural = 'tickets'

    def qr_generate(self) -> None:
        img = qrcode.make(f'https://{Site.objects.get_current().domain}/api/v1/ticket/{self.uuid}')
        buf = io.BytesIO()
        img.save(buf, "PNG")
        self.qr_code.save(f'qr_code-{self.uuid}', File(buf), save=False)
        return None

    def save(self, *args, **kwargs):
        from django.core.exceptions import ValidationError
        if not self.qr_code:
            self.qr_generate()
        same_ticket = self.event.tickets.filter(number=self.number)
        if same_ticket and self.uuid != same_ticket.first().uuid:
            raise ValidationError('Same number created')
        return super().save()

    def __str__(self):
        return f'{self.number}'
