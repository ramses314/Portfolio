from django.contrib.sites.models import Site
from rest_framework import serializers

from . import mixins, models
from .utils import event_all_fields


class PrizeDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Prize
        fields = '__all__'


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = [
            'id',
            'title',
            'events',
        ]


class EventListSerializer(
        mixins.GetPPCMixin,
        serializers.ModelSerializer,
):
    category = CategoryDetailSerializer()
    prizes = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    counter = serializers.SerializerMethodField()

    class Meta:
        model = models.Event
        fields = event_all_fields() + ['price', 'counter', 'prizes']


class EventWinnersListSerializer(
        mixins.GetPPCMixin,
        mixins.GetTicketsMixin,
        serializers.ModelSerializer,
):
    category = CategoryDetailSerializer()
    tickets = serializers.SerializerMethodField()
    prizes = serializers.SerializerMethodField()

    class Meta:
        model = models.Event
        fields = event_all_fields() + ['prizes', 'tickets']


class EventDetailSerializer(
        mixins.GetPPCMixin,
        mixins.GetTicketsMixin,
        serializers.ModelSerializer,
):
    tickets = serializers.SerializerMethodField()
    prizes = serializers.SerializerMethodField()
    category = CategoryDetailSerializer()
    price = serializers.SerializerMethodField()
    counter = serializers.SerializerMethodField()
    winners = serializers.SerializerMethodField()

    class Meta:
        model = models.Event
        needed_fields = event_all_fields()
        fields = event_all_fields() + ['price', 'counter', 'prizes', 'winners', 'tickets']

    def get_winners(self, obj):
        return [{'uuid': i.uuid, 'number': i.number} for i in obj.tickets.filter(is_winner=True)]


class EventSocketSerializer(serializers.ModelSerializer):
    event = serializers.SerializerMethodField()
    prizes = serializers.SerializerMethodField()
    category = CategoryDetailSerializer()

    class Meta:
        model = models.Event
        fields = [
            'event',
            'prizes',
            'category',
        ]

    def get_event(self, obj: models.Event):
        try:
            return {
                'id': obj.pk,
                'title': obj.title,
                'slug': obj.slug,
                'content': obj.content,
                'expired': f'{obj.expired}',
                'image': obj.image.url if obj.image else 'null',
                'ticket_quantity': obj.ticket_quantity,
                'link': obj.link,
            } # yapf:disable
        except AttributeError:
            return None

    def get_prizes(self, obj):
        prizes = obj.prizes.all()
        serializer = PrizeDetailSerializer(prizes, many=True, read_only=True)
        return serializer.data


class TicketDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Ticket
        exclude = ['order']


class TicketSocketSerializer(serializers.ModelSerializer):
    ticket = serializers.SerializerMethodField()

    class Meta:
        model = models.Ticket
        fields = ['ticket']

    def get_ticket(self, obj: models.Ticket):
        ticket = {
            'uuid': f'{obj.uuid}',
            'status': obj.get_status_display(),
            'event': obj.event.id,
            'number': obj.number,
            'price': f'{obj.price}',
            'qr_code': obj.qr_code.url,
        }
        if hasattr(obj, 'order'):
            if obj.order is not None:
                ticket['user_uuid'] = f'{obj.order.user_uuid}'
        return ticket
