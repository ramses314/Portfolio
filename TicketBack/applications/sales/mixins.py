
from .models import Order
from ..main.models import Preference
from rest_framework import serializers


class ValidateFrontUUIDMixin:

    @staticmethod
    def validate_front_uuid(value):
        preference: Preference = Preference.objects.first()
        if preference and str(preference.front_uuid) in value:
            return value
        raise serializers.ValidationError('front_uuid incorrect')

    def create(self, validated_data):
        pass

    def update(self, validated_data):
        pass


class ValidateUserUUIDMixin:

    def validate_user_uuid(self, value):
        order = Order.objects.filter(user_uuid=value).first()
        if order:
            if order.status == 'payed':
                raise serializers.ValidationError('order was completed')
            return value
        raise serializers.ValidationError({
            'error': 'user_uuid incorrect (order does not exist)'
        })
