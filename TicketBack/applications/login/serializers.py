import uuid

from dj_rest_auth.serializers import LoginSerializer as DjRestAuthLoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer, VerifyEmailSerializer
from rest_framework import serializers

from applications.login.adapters import AuthenticationAdapter, CleanedDataAdapter
from applications.sales.mixins import ValidateFrontUUIDMixin
from applications.users.models import CustomUser


class CustomVerifyEmailSerializer(
    VerifyEmailSerializer,
    ValidateFrontUUIDMixin,
):
    front_uuid = serializers.CharField(max_length=255)


class CustomRegisterSerializer(
    RegisterSerializer,
    ValidateFrontUUIDMixin,
):
    front_uuid = serializers.CharField(max_length=255)
    username = serializers.HiddenField(default=f'{uuid.uuid4()}')
    phone_number = serializers.CharField(max_length=25)
    first_name = serializers.CharField(max_length=25)
    last_name = serializers.CharField(max_length=25)

    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()
        return CleanedDataAdapter(self).get_cleaned_data(cleaned_data)

    def save(self, request):
        user = super().save(request)
        user.phone_number = self.validated_data.get('phone_number')
        user.save()
        return user


class LoginSerializer(DjRestAuthLoginSerializer):
    username = serializers.HiddenField(required=False, default=None)
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        user = CustomUser.objects.filter(email=email).first()

        auth_adapter = AuthenticationAdapter(user)
        attrs = auth_adapter.authenticate(attrs)
        return attrs
