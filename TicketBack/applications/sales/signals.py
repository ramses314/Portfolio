import datetime

from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .models import Order
from .serializers import OrderSocketSerializer
from ..core.jsons import json_socket_response
from ..main.models import TestBlock


@receiver(post_save, sender=Order)
def order_post_save_message(sender, instance, **kwargs):
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer
    from ..events.models import Client
    channel_layer = get_channel_layer()
    client = Client.objects.filter(request_id__startswith=f'order_{instance.user_uuid}').first()
    if client:
        async_to_sync(channel_layer.group_send)(
            client.request_id,
            json_socket_response(channel='order', type='u', body=OrderSocketSerializer(instance).data, client=client)
        )


@receiver(pre_delete, sender=Order)
def order_pre_delete_message(sender, instance, **kwargs):
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer

    from ..events.models import Client
    channel_layer = get_channel_layer()
    client = Client.objects.filter(request_id__startswith=f'order_{instance.user_uuid}').first()
    order = instance
    event = order.tickets.first().event if order.tickets.exists() else None
    numbers_of_tickets = [t.number for t in order.tickets.only('number')] if event else []
    if client:
        body = {
            'message': 'deleted: Null tickets on this order',
            'event_slug': event.slug if event else None,
            'numbers_of_ticket': numbers_of_tickets,
        }
        ticket = instance.tickets.first()
        if ticket:
            body['message'] = 'deleted: This tickets open again'
        async_to_sync(channel_layer.group_send)(
            client.request_id,
            json_socket_response(channel='order', type='i', body=body, client=client)
        )


@receiver(pre_delete, sender=Order)
def order_delete_message_again_open_tickets(sender, instance, **kwargs):
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer

    from ..events.models import Client
    order = instance
    event = order.tickets.first().event if order.tickets.exists() else None
    numbers_of_tickets = [t.number for t in order.tickets.only('number')] if event else []
    channel_layer = get_channel_layer()
    clients = Client.objects.filter(request_id__startswith=f'ticket_')

    if clients and event:
        event_info = 'This tickets open again'
        body = {
            'message': event_info,
            'event_slug': event.slug,
            'numbers_of_ticket': numbers_of_tickets,
        }
        for client in clients:
            async_to_sync(channel_layer.group_send)(
                client.request_id,
                json_socket_response(channel='ticket', type='i', body=body, client=client))


@receiver(post_save, sender=Order)
def order_expired(sender, instance, **kwargs):
    from jobs.jobs import jobs_order_expired
    from applications.main.apps import MainConfig
    from ..events.utils import remove_jobs_try

    order = instance
    scheduler = MainConfig.scheduler
    remove_jobs_try(scheduler, f'order_expired_{order.uuid}')
    tb = TestBlock.objects.first()

    if tb is None or tb and not tb.order_expired:
        if order.status in ['waiting', 'blocked']:
            start_date = datetime.datetime.now() + datetime.timedelta(minutes=10)
            scheduler.add_job(
                jobs_order_expired,
                'date',
                run_date=start_date,
                id=f'order_expired_{order.uuid}',
                kwargs={'order': order}
            )
