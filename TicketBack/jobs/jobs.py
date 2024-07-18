
from applications.sales.models import Order




def jobs_event_date_expired(**kwargs):
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer
    from applications.core.jsons import json_socket_response
    from applications.events.models import Client

    event = kwargs['event']
    channel_layer = get_channel_layer()
    clients = Client.objects.filter(request_id__startswith='event_')
    if clients:
        event_inform = 'Event is expired'
        body = {
            'message': event_inform,
            'event_slug': event.slug
        }
        for client in clients:
            async_to_sync(channel_layer.group_send)(
                client.request_id,
                json_socket_response(
                    channel='event',
                    type='i', body=body,
                    client=client
                )
            )


def jobs_order_expired(**kwargs):
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer
    from applications.core.jsons import json_socket_response
    from applications.events.models import Client

    order = Order.objects.get(uuid=kwargs['order'].uuid)
    channel_layer = get_channel_layer()
    client_order = Client.objects.filter(request_id__startswith=f'order_{order.user_uuid}').first()
    clients_ticket = Client.objects.filter(request_id__startswith='ticket_')

    event = order.tickets.first().event if order.tickets.exists() else None
    numbers_of_tickets = [t.number for t in order.tickets.only('number')] if event else None
    order_uuid = order.uuid

    if order.status != Order.Status.PAYED:
        order.tickets.all().update(status='open', order=None)
        order.delete()

        if client_order and Order.objects.filter(uuid=order.uuid).first():
            order_inform = 'Order is expired and disbanded'
            body = {
                'message': order_inform,
                'order_uuid': f'{order_uuid}'
            }
            async_to_sync(channel_layer.group_send)(
                client_order.request_id,
                json_socket_response(
                    channel='order',
                    type='i',
                    body=body,
                    client=client_order
                )
            )

        if clients_ticket and event:
            event_inform = 'This tickets open again'
            body = {
                'message': event_inform,
                'event_slug': event.slug,
                'numbers_of_ticket': numbers_of_tickets,
            }
            for client in clients_ticket:
                async_to_sync(channel_layer.group_send)(
                    client.request_id,
                    json_socket_response(
                        channel='ticket',
                        type='i', body=body,
                        client=client
                    )
                )
