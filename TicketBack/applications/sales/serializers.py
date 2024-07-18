import datetime
import uuid

from rest_framework import serializers

from .models import Order
from ..core.jsons import get_order_json, get_event_with_tickets_json
from ..events.models import Ticket

from . import models
from . import mixins


class OrderSerializer(serializers.ModelSerializer):

    tickets = serializers.SerializerMethodField()

    class Meta:
        model = models.Order
        fields = '__all__'

    def get_tickets(self, obj):
        events = list(set([i.event for i in obj.tickets.all()]))
        main_json = []
        for event in events:
            tickets = obj.tickets.filter(event_id=event.id)
            main_json.append(get_event_with_tickets_json(event, tickets))
        return main_json


class AddProductSerializer(
    mixins.ValidateFrontUUIDMixin,
    serializers.Serializer,
):
    front_uuid = serializers.CharField(max_length=225)
    ticket_uuid = serializers.CharField(max_length=255)
    user_uuid = serializers.CharField(max_length=225)

    def validate_ticket_uuid(self, value):
        ticket = Ticket.objects.only('uuid').filter(uuid=value).first()
        if not ticket:
            raise serializers.ValidationError({
                'error': 'ticket_uuid incorrect'
            })
        elif ticket.status in ['blocked', 'sold']:
            raise serializers.ValidationError({
                'error': f'ticket is {ticket.status}'
            })
        elif ticket.event.expired.replace(tzinfo=None) < datetime.datetime.now():
            raise serializers.ValidationError({
                'error': 'Event is expired'
            })
        return value


class DeleteProductSerializer(
    mixins.ValidateFrontUUIDMixin,
    mixins.ValidateUserUUIDMixin,
    serializers.Serializer,
):
    front_uuid = serializers.CharField(max_length=225)
    ticket_uuid = serializers.CharField(max_length=255)
    order_uuid = serializers.CharField(max_length=255)
    user_uuid = serializers.CharField(max_length=225)

    def validate_ticket_uuid(self, value):
        if Ticket.objects.only('uuid').filter(uuid=value).first():
            return value
        raise serializers.ValidationError({
                'error': 'ticket_uuid incorrect'
        })

    def validate_order_uuid(self, value):
        if Order.objects.only('uuid').filter(uuid=value).first():
            return value
        raise serializers.ValidationError({
                'error': 'order_uuid incorrect'
        })

    def validate(self, attr):
        order = Order.objects.filter(uuid=attr['order_uuid'], user_uuid=attr['user_uuid']).first()
        ticket = Ticket.objects.only('uuid', 'order').filter(uuid=attr['ticket_uuid']).first()
        if order:
            if ticket.order != order:
                raise serializers.ValidationError({
                    'error': 'ticket not belong to order'
                })
            return attr
        raise serializers.ValidationError({
            'error': 'user_uuid not belong to this order'
        })


class UpdateTokenOrderSerializer(
    mixins.ValidateFrontUUIDMixin,
    serializers.Serializer,
):

    front_uuid = serializers.CharField(max_length=225)
    user_uuid = serializers.CharField(max_length=225)
    name = serializers.CharField(max_length=225)
    email = serializers.CharField(max_length=225)
    phone = serializers.CharField(max_length=500)

    card_token = serializers.CharField(max_length=255)
    payment_method_id = serializers.CharField(max_length=255)

    def validate(self, attr):
        order = Order.objects.filter(user_uuid=attr['user_uuid']).first()
        if not order:
            raise serializers.ValidationError('order does not exists')
        elif order.tickets.all().count() == 0:
            raise serializers.ValidationError('order is empty')
        return attr


class OrderSocketSerializer(serializers.ModelSerializer):
    order = serializers.SerializerMethodField()

    class Meta:
        model = models.Order
        fields = ['order']

    def get_order(self, obj: models.Order):
        try:
            tickets = obj.tickets.all()
            return get_order_json(obj, tickets)
        except AttributeError:
            return None


class OrderGetSerializer(serializers.Serializer):

    uuid = serializers.CharField(max_length=255)

    def validate_uuid(self, value):
        try:
            uuid.UUID(str(value))
            if not Order.objects.only('uuid').filter(uuid=value):
                raise serializers.ValidationError({
                    'error': 'incorrect order_uuid'
                })
        except ValueError:
            raise serializers.ValidationError({
                'error': "order_uuid: it's not uuid"
            })
        return value
