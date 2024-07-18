from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from applications.core.mail import EmailFactory, HTMLMessageContext
from applications.main.models import Preference


class CustomAllauthAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        front_url = (
            Preference.objects.first().front_url) if Preference.objects.first() else 'http://example.com'

        if 'activate_url' in context:
            url = context['activate_url'].split("/")
            EmailFactory(email).send_html_email(
                subject='confirmación de registro',
                template_path='login/registration.html',
                context=HTMLMessageContext(
                    email=email, redirect_url=front_url.rstrip("/") + "/login/confirm?key=" + url[-2]
                ).return_dict()
            )

        elif 'password_reset_url' in context:
            url = context['password_reset_url'].split("/")
            EmailFactory(email).send_html_email(
                subject='recuperación de contraseña',
                template_path='login/reset_password.html',
                context=HTMLMessageContext(
                    email=email,
                    redirect_url=front_url.rstrip("/") + "/login/password-reset" + f"?uid={url[-3]}" + f"&token={url[-2]}"
                ).return_dict()
            )


class AuthenticationAdapter:
    def __init__(self, user):
        self.user = user

    def authenticate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            if not self.user:
                msg = _('Invalid credentials. Email not registered')
                raise serializers.ValidationError(msg, code='authorization')

            if not self.user.is_active:
                msg = _("User inactive. Please confirm your account in email.")
                raise serializers.ValidationError(msg, code='authorization')

            if not check_password(password, self.user.password):
                msg = _('Invalid credentials. Please try again.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Fill the required fields.')
            raise serializers.ValidationError(msg, code='authorization')

        self.user.backend = 'django.contrib.auth.backends.ModelBackend'
        attrs['user'] = self.user

        return attrs


class CleanedDataAdapter:
    def __init__(self, serializer):
        self.serializer = serializer

    def get_cleaned_data(self, cleaned_data):
        cleaned_data.update({
            'first_name': self.serializer.validated_data.get('first_name', ''),
            'last_name': self.serializer.validated_data.get('last_name', ''),
            'password1': self.serializer.validated_data.get('password1', ''),
            'email': self.serializer.validated_data.get('email', ''),
            'phone_number': self.serializer.validated_data.get('phone_number', '')
        })
        return cleaned_data
