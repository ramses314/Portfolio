import hashlib

from django.conf import settings
from rest_framework import serializers, pagination
from applications.users.models import CustomUser
from applications.core.jsons import get_tickets_for_profile

from applications.sales.models import Order, PaymentTokenService
from applications.sales.serializers import OrderSerializer


class GoogleSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=255)
    client_id = serializers.CharField(max_length=255)
    secret_key = serializers.CharField(max_length=255)

    def validate(self, attrs):

        hashed_value = hashlib.md5(settings.GOOGLE_OAUTH2_CLIENT_SECRET.encode()).hexdigest()

        if attrs['secret_key'] not in [settings.GOOGLE_OAUTH2_CLIENT_SECRET, hashed_value]:
            raise serializers.ValidationError({
                'error': 'secret_key is incorrect'
            })
        elif attrs['client_id'] != settings.GOOGLE_OAUTH2_CLIENT_ID:
            raise serializers.ValidationError({
                'error': 'client_id is incorrect'
            })
        return attrs


class UserOrderSerializer(
    OrderSerializer
):

    class Meta:
        model = Order
        fields = [
            'uuid',
            'user_uuid',
            'status',
            'created',
            'modified',
            'name',
            'phone',
            'email',
            'description',
            'add_hash',
            'tickets',
        ]

    def get_tickets(self, obj):
        events = list(set([i.event for i in obj.tickets.all()]))
        main_json = []
        for event in events:
            tickets = obj.tickets.filter(event_id=event.id)
            main_json.append(get_tickets_for_profile(event, tickets))
        return main_json


class UserProfileSerializer(serializers.ModelSerializer):

    count = serializers.SerializerMethodField()
    orders = serializers.SerializerMethodField()
    payment_token = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'image',
            'count',
            'phone',
            'payment_token',
            'orders',
        ]

    def get_phone(self, obj):
        exists = Order.objects.filter(user_uuid=obj['username']).exclude(phone__isnull=True)\
            .exclude(phone__exact='').first()
        return exists.phone if exists else None

    def get_count(self, obj):
        return Order.objects.filter(user_uuid=obj['username']).count()

    def get_payment_token(self, obj):
        user = CustomUser.objects.get(email=obj['email'])
        token = PaymentTokenService.objects.filter(user=user).first()
        json = {'status': 'exists', 'card_last_digits': token.last_digits} if token else False
        return json

    def get_orders(self, obj):
        username = obj['username']
        orders_from_user = Order.objects.filter(user_uuid=username).order_by('-created')
        paginator = pagination.PageNumberPagination()
        paginator.page_query_param = 'track_page'
        paginator.page_size_query_param = 'track_page_size'
        paginator.page_size = 10
        page = paginator.paginate_queryset(
            orders_from_user,
            obj['request'],
        )
        serializer = UserOrderSerializer(
            page,
            many=True,
            context={'request': obj['request']},
        )
        return paginator.get_paginated_response(serializer.data).data
