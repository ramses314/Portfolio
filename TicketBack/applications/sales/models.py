import uuid

from django.db import models
from django.db.models import Sum

from applications.core.models import Condition, Single, PathAndRename, Common
from django.contrib.sites.models import Site

from applications.main.models import Preference
from applications.users.models import CustomUser


class Order(Condition):
    """
    Order
    """

    user_uuid = models.CharField(
        verbose_name='USER Unique id',
        max_length=255,
        null=True,
    )

    uuid = models.UUIDField(
        verbose_name='Unique id',
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )

    class Status(models.TextChoices):
        PURCHASE = 'purchase', 'purchase'
        WAITING = 'waiting', 'waiting'
        BLOCKED = 'blocked', 'blocked'
        PAYED = 'payed', 'payed'

    status = models.CharField(
        verbose_name='Status',
        max_length=10,
        choices=Status.choices,
        default=Status.WAITING,
    )

    created = models.DateTimeField(
        verbose_name='Created date',
        auto_now_add=True,
    )

    modified = models.DateTimeField(
        verbose_name='Modified',
        auto_now=True,
    )

    name = models.CharField(
        verbose_name='Name',
        max_length=255,
        blank=True,
    )

    phone = models.CharField(
        verbose_name='Phonenumber',
        max_length=255,
        blank=True,
    )

    email = models.CharField(
        verbose_name='Email',
        max_length=255,
        blank=True,
    )

    description = models.TextField(
        verbose_name='Description',
        blank=True,
        null=True,
    )

    admin_comment = models.TextField(
        verbose_name='Admin comment',
        blank=True,
        null=True,
    )

    payment = models.CharField(
        verbose_name='Link payment',
        max_length=500,
        blank=True,
        null=True,
    )

    token_trans = models.CharField(
        verbose_name='token_trans',
        max_length=255,
        blank=True,
        null=True,
    )

    redirect_url = models.CharField(
        verbose_name='redirect_url',
        max_length=255,
        blank=True,
        null=True,
    )

    add_hash = models.CharField(
        max_length=16,
        verbose_name='Add hash',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def mail_client(self):
        from django.conf import settings
        from django.core.mail import send_mail
        from django.template.loader import render_to_string
        from applications.core.jsons import get_tickets_for_letter

        events = list(set([i.event for i in self.tickets.all()]))
        main_json = []
        for event in events:
            main_json.append(get_tickets_for_letter(event, self))

        front_url = Preference.objects.first().front_url
        tickets = self.tickets.filter().first()
        domain = Site.objects.get_current()
        context = {
            'object': self,
            'check_link': f'{front_url}/check?order={self.uuid}',
            'domain': domain,
            'images': LetterImage.objects.first(),
            'front_url': front_url
        }
        if tickets:
            context.update({
                'amount': self.amount,
                'add_hash': self.add_hash,
                'main_json': main_json,
            })
        html_message = render_to_string('sales/letter_order.html', context)
        return send_mail(
            subject='¡Tus Tickets digitales están aquí!',
            message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email],
            html_message=html_message,
        )

    def delete(self, *args, **kwargs):
        from ..events.models import Ticket
        self.tickets.update(status=Ticket.Status.OPEN)
        return super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.uuid}'

    @property
    def amount(self):
        return self.tickets.all().aggregate(amount=Sum('price')).get('amount')


class LetterImage(Single):
    """
    Images for letter after pay
    """

    title = models.CharField(
        verbose_name='Title',
        max_length=255,
    )

    image_logo = models.ImageField(
        verbose_name='Logo TicketCrush',
        upload_to=PathAndRename('sales/letter/images'),
        blank=True,
        null=True,
    )

    image_ticket_left = models.ImageField(
        verbose_name='Tickets left',
        upload_to=PathAndRename('sales/letter/images'),
        blank=True,
        null=True,
    )

    image_ticket_right = models.ImageField(
        verbose_name='Tickets right',
        upload_to=PathAndRename('sales/letter/images'),
        blank=True,
        null=True,
    )

    image_youtube_logo = models.ImageField(
        verbose_name='Youtube',
        upload_to=PathAndRename('sales/letter/images'),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'LetterImage'
        verbose_name_plural = 'LetterImage'

    def __str__(self):
        return 'LetterImage'


class PaymentTokenService(Common):
    """
    PaymentTokenService
    """

    user = models.OneToOneField(
        verbose_name='User',
        to=CustomUser,
        on_delete=models.CASCADE
    )

    token = models.CharField(
        verbose_name='Token',
        max_length=255,
        null=True,
        blank=True
    )

    last_digits = models.CharField(
        verbose_name='Last digits',
        max_length=4,
    )

    class Meta:
        verbose_name = 'Service payment token'
        verbose_name_plural = 'Service payment token'

    def __str__(self):
        return self.last_digits


class MercadoPago(Single):
    """
    Model for payment
    """

    access_token = models.CharField(
        verbose_name='ACCESS TOKEN',
        max_length=255,
        default='set_your',
    )

    public_key = models.CharField(
        verbose_name='PUBLIC KEY',
        max_length=255,
        default='set_your'
    )

    class Meta:
        verbose_name = 'Mercado Pago'
        verbose_name_plural = 'Mercado Pago'

    def __str__(self):
        return 'MercadoPago'
