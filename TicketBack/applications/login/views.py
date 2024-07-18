from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from dj_rest_auth.views import LoginView as RestAuthLoginView, PasswordResetView
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from applications.login.serializers import CustomVerifyEmailSerializer
from applications.sales.models import PaymentTokenService
from applications.users.models import CustomUser


class CustomLoginView(RestAuthLoginView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = CustomUser.objects.filter(email=request.data['email']).first()
        self.add_refresh_token(response, user)
        self.add_payment_info(response, user)
        return response

    @staticmethod
    def add_refresh_token(response, user):
        refresh_token = RefreshToken.for_user(user)
        response.data['refresh_token'] = str(refresh_token)

    @staticmethod
    def add_payment_info(response, user):
        token = PaymentTokenService.objects.filter(user=user).first()
        json = {'status': 'exists', 'card_last_digits': token.last_digits} if token else False
        response.data['user']['payment_token'] = json


class CustomRegisterView(RegisterView):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        user.is_active = False
        user.save()
        return Response(
            self.get_response_data(user),
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data),
        )


class CustomVerifyEmail(VerifyEmailView):

    def post(self, request, *args, **kwargs):
        serializer = CustomVerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        self.change_user_active(confirmation.email_address.user)
        return Response({'detail': _('ok')}, status=status.HTTP_200_OK)

    @staticmethod
    def change_user_active(user):
        user.is_active = True
        user.save()


class CustomPasswordResetView(PasswordResetView):
    def post(self, request, *args, **kwargs):
        email = self.request.data.get('email')
        if not CustomUser.objects.filter(email=email).first():
            return Response({"detail": "User not found."}, status=status.HTTP_400_BAD_REQUEST)

        return super().post(request, *args, **kwargs)
