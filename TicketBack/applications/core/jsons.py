from datetime import datetime
from applications.events.models import Event

from typing import Dict, List

from applications.events.models import Ticket
from applications.sales.models import Order


# FOR GENERAL

def json_socket_response(channel, type, body, client):

    response = {
        'type': 'chat_message',
        'message': {
            'channel': channel,
            'data': {
                'type': type,
                'body': body,
                'request_id': str(client.request_id).split('_')[1]
            },

            'status': 200,
        }
    }
    return response


# FOR EVENT

def get_ticket_json(tickets: list) -> dict:
    tickets_json = []

    for ticket in tickets:
        ticket_json = {
            'uuid': f'{ticket.uuid}',
            'status': ticket.get_status_display(),
            'event': ticket.event.id,
            'number': ticket.number,
            'price': f'{ticket.price}',
            'qr_code': ticket.qr_code.url,
        }
        tickets_json.append(ticket_json)
    return tickets_json


def get_event_json(event: Event) -> dict:
    event_json = []
    if event:
        event_json = {
            'title': event.title,
            'slug': event.slug,
            'event_expired': event.expired,
            'image': event.image.url if event.image else None,
            'content': event.content,
            'price': event.price,
            'event_time': event.time_event
        }
    return event_json


def get_event_with_tickets_json(event: Event, tickets: List[Ticket]) -> dict:
    event_json = []
    if event:
        event_json = {
            'title': event.title,
            'slug': event.slug,
            'image': event.image.url if event.image else None,
            'content': event.content,
            'tickets': get_ticket_json(tickets),
        }
    return event_json


def get_tickets_for_profile(event: Event, tickets: List[Ticket]) -> dict:
    event_json = []
    if event:
        event_json = {
            'title': event.title,
            'slug': event.slug,
            'image': event.image.url if event.image else None,
            'content': event.content,
            'expired': event.expired,
            'time_event': event.time_event,
            'winner_numbers': [{
                    'number': i.number,
                    'prize_id': i.prize_id.id if i.prize_id else None} for i in event.tickets.filter(is_winner=True)],
            'prizes': [],
            'user_tickets': get_ticket_json(tickets),
        }

        for prize in event.prizes.all():
            image_url = prize.image.url if prize.image else None
            event_json['prizes'].append(
                {
                    'id': prize.id,
                    'title': prize.title,
                    'content': prize.content,
                    'image': image_url
                })
    return event_json


def get_tickets_for_letter(event: Event, order) -> dict:
    event_json = []

    if event:
        tickets = order.tickets.filter(event=event)
        event_json = {
            'title': event.title,
            'slug': event.slug,
            'expired': event.expired,
            'time_event': event.time_event,
            'price': event.tickets.first().price,
            'numbers': [t.number for t in tickets],
            'link': event.link,
        }

    return event_json


# FOR ORDER

def pagadito_template_for_send_order(
        order: Order,
        card: dict,
        tickets: List[Ticket]

):
    order_template = {
            "card": {
                "number": card['number'],
                "expirationDate": card['date'],
                "cvv": card['cvv'],
                "cardHolderName": card['name'],
                "firstName": "John",
                "lastName": "Smith",
                "billingAddress": {
                    "city": "San Salvador",
                    "state": "San Salvador",
                    "zip": "",
                    "countryId": "740",
                    "line1": "7a calle poniente bis",
                    "phone": "+503 7777 8888"
                },
                "email": "johnsmith@correo.com"
            },

            "transaction": {
                "merchantTransactionId": str(order.uuid),
                "currencyId": "USD",
                "transactionDetails": [
                    {
                        "quantity": "1",
                        "description": str(ticket.event.title),
                        "amount": str(ticket.price)
                    } for ticket in tickets
                ]
            },

            "browserInfo": {
                "deviceFingerprintID": "1679136332496",
                "customerIp": "185.117.148.58"
            }
        }
    return order_template


def pagadito_token_template_for_send_order(
        order: Order,
        token,
        tickets: List[Ticket]

):
    order_template = {
            "payment_token": str(token),
            "transaction": {
                "merchantTransactionId": str(order.uuid),
                "currencyId": "USD",
                "transactionDetails": [
                    {
                        "quantity": "1",
                        "description": "Pair of Red Shoes Size 8",
                        "amount": str(ticket.price)
                    } for ticket in tickets
                ]
            },

            "browserInfo": {
                "deviceFingerprintID": "1679136332496",
                "customerIp": "185.117.148.58"
            }
        }
    return order_template


def get_order_json(obj, tickets):

    order = {
        'user_uuid': f'{obj.user_uuid}',
        'uuid': f'{obj.uuid}',
        'status': obj.get_status_display(),
        'name': obj.name,
        'email': obj.email,
        'description': obj.description,
        'tickets': get_ticket_json(tickets),
    }

    return order


def json_winner_response(event, tickets):
    event_json = []
    if event:
        response_status = 'winner' if tickets.filter(is_winner=True) else 'not winner'
        event_json = {
            'status': response_status
            if event.expired.replace(tzinfo=None) < datetime.now() else 'Event not passed yet',
            'event': get_event_json(event),
            'winner_numbers': [{
                'number': i.number,
                'prize_id': i.prize_id.id if i.prize_id else None} for i in event.tickets.filter(is_winner=True)],
            'prizes': [],
            'user_tickets': [t.number for t in tickets],
        }

        for prize in event.prizes.all():
            image_url = prize.image.url if prize.image else None
            event_json['prizes'].append(
                {
                    'id': prize.id,
                    'title': prize.title,
                    'content': prize.content,
                    'image': image_url
                })

    return event_json
