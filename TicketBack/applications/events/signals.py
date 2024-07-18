
from channels.layers import get_channel_layer
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Event, Ticket
from ..core.jsons import json_socket_response


@receiver(post_save, sender=Event)
def event_post_save_message(sender, instance, **kwargs):
    from asgiref.sync import async_to_sync
    from .models import Client
    from applications.events.serializers import EventSocketSerializer

    channel_layer = get_channel_layer()
    clients = Client.objects.filter(request_id__startswith='event_')
    if clients:
        for client in clients:
            async_to_sync(channel_layer.group_send)(
                client.request_id,
                json_socket_response(
                    channel='event',
                    type='u',
                    body=EventSocketSerializer(instance).data,
                    client=client
                )
            )


@receiver(post_save, sender=Ticket)
def ticket_post_save_message(sender, instance, **kwargs):
    from applications.events.serializers import TicketSocketSerializer
    from asgiref.sync import async_to_sync
    from .models import Client
    channel_layer = get_channel_layer()
    clients = Client.objects.filter(request_id__startswith='ticket_')
    if clients:
        for client in clients:
            async_to_sync(channel_layer.group_send)(
                client.request_id,
                json_socket_response(
                    channel='ticket',
                    type='u',
                    body=TicketSocketSerializer(instance).data,
                    client=client
                )
            )


@receiver(post_save, sender=Ticket)
def event_all_tickets_are_sold(sender, **kwargs):
    from asgiref.sync import async_to_sync
    from .models import Client

    ticket = kwargs['instance']
    event = ticket.event
    tickets_have = event.tickets.all().filter(status='open')

    if not tickets_have:
        channel_layer = get_channel_layer()
        clients = Client.objects.filter(request_id__startswith='event_')
        if clients:
            event_info = f'All tickets are sold in event'
            for client in clients:
                body = {
                    'message': event_info,
                    'event_slug': event.slug,
                }
                async_to_sync(channel_layer.group_send)(
                    client.request_id,
                    json_socket_response(channel='event', type='i', body=body, client=client)
                )


@receiver(pre_save, sender=Ticket)
def send_variable_number_of_open_tickets(sender, instance, **kwargs):
    from asgiref.sync import async_to_sync
    from .models import Client

    old_instance = sender.objects.filter(pk=instance.pk)
    if old_instance and old_instance.first().status != 'sold' and instance.status == 'sold':
        ticket = instance
        event = ticket.event
        channel_layer = get_channel_layer()
        clients = Client.objects.filter(request_id__startswith='event_')
        if clients:
            message = f'ticket is sold'
            for client in clients:
                body = {
                    'message': message,
                    'event_slug': event.slug,
                    'counter': event.tickets.filter(status='open').count()
                }
                async_to_sync(channel_layer.group_send)(
                    client.request_id,
                    json_socket_response(channel='event', type='i', body=body, client=client)
                )


@receiver(post_save, sender=Event)
def event_date_is_expired(sender, **kwargs):
    from jobs.jobs import jobs_event_date_expired
    from applications.main.apps import MainConfig
    from .utils import remove_jobs_try

    event = kwargs['instance']
    scheduler = MainConfig.scheduler
    remove_jobs_try(scheduler, f'event_expired_{event.id}')

    scheduler.add_job(
        jobs_event_date_expired,
        'date',
        run_date=event.expired,
        id=f'event_expired_{event.id}',
        kwargs={'event': event}
    )


@receiver(pre_save, sender=Event)
def event_change_ticket_price(sender, instance, **kwargs):
    event = instance
    tickets_to_update = event.tickets.all() if event.pk else None
    old_instance = sender.objects.filter(pk=instance.pk)

    if event.pk and (old_instance and old_instance.first().price != instance.price):
        tickets_to_update.update(price=event.price)
        tickets_to_update.update(price=event.price)
        Ticket.objects.bulk_update(tickets_to_update, ['price'])
