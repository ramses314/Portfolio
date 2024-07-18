import datetime
import json
import requests
import jwt

from django.db import transaction
from django.core.management.utils import get_random_secret_key
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from applications.users.models import CustomUser as User, CustomUser
from applications.sales.models import PaymentTokenService


def jwt_login(*, user: User) -> dict:

    User = get_user_model()
    user = User.objects.get(id=user.id)
    access_token = AccessToken.for_user(user)
    refresh_token = RefreshToken.for_user(user)
    decoded_token = jwt.decode(str(access_token), settings.SECRET_KEY, algorithms=["HS256"], verify=True)

    user_record_login(user=user)

    response = {
        'access_token': str(access_token),
        'refresh_token': str(refresh_token),
        'expired': datetime.datetime.fromtimestamp(decoded_token['exp']),
        'user': None
    }

    return response


def google_validate_id_token(*, id_token: str):
    response = requests.get(
        'https://www.googleapis.com/oauth2/v3/tokeninfo',
        params={'id_token': id_token}
    )

    if not response.ok:
        raise ValidationError('id_token is invalid.')

    audience = response.json()['aud']

    if audience != settings.GOOGLE_OAUTH2_CLIENT_ID:
        raise ValidationError('Invalid audience.')

    return response.json()


def user_create(email, password=None, **extra_fields) -> User:
    extra_fields = {
        'is_staff': False,
        'is_superuser': False,
        **extra_fields
    }

    user = User(email=email, **extra_fields)

    if password:
        user.set_password(password)
    else:
        user.set_unusable_password()

    user.full_clean()
    user.save()

    return user


def user_create_superuser(email, password=None, **extra_fields) -> User:
    extra_fields = {
        **extra_fields,
        'is_staff': True,
        'is_superuser': True
    }
    user = user_create(email=email, password=password, **extra_fields)
    return user


def user_record_login(*, user: User) -> User:
    user.last_login = timezone.now()
    user.save()
    return user


def user_get_or_create(email, first_name, last_name, image=None):

    User = get_user_model()

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            image=image,
        )

    return user


def get_user_by_token(access_token):

    User = get_user_model()

    try:
        decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"], verify=True)
        user_id = decoded_token['user_id']
        user = User.objects.filter(id=user_id).first()
        return user
    except Exception as e:
        raise AuthenticationFailed({
            'error': 'token is invalid'
        })


def renew_user(user, serializer):
    full_name = serializer.validated_data.get('name')
    if full_name and not (user.first_name and user.last_name):
        names = full_name.split()
        user.first_name = names[0]
        user.last_name = names[1] if len(names) > 1 else ''
        user.save()


def user_have_token(user: CustomUser):

    if user:
        token = PaymentTokenService.objects.filter(user=user).first()
        if token and str(token.token).startswith('cus_'):
            return True
    return False


def user_check_auth(request):

    auth_token = request.headers.get('Authorization')

    if not auth_token:
        raise AuthenticationFailed('Authorization header not found')

    if str(auth_token).startswith('Bearer'):
        auth_token = auth_token.split(' ')[1]

    user = get_user_by_token(auth_token)

    if not user:
        return Response({'error': 'token is not valid'})

    return user


def record_payment_token(user, token, serializer):
    digits = serializer.validated_data.get('card_number')
    if digits:
        PaymentTokenService.objects.create(
            user=user,
            token=token,
            last_digits=digits[-4:]
        )


def load_creds_json(redirect):
    clean_creds_json()

    with open('client_secrets.json', 'r') as f:
        data = json.load(f)

    creds = {
        'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
        'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
        'redirect_uri': redirect,
        'auth_uri': settings.GOOGLE_OAUTH2_AUTH_URL,
        'token_uri': settings.GOOGLE_OAUTH2_TOKEN_URL
    }

    data['web'] = creds

    with open('client_secrets.json', 'w') as f:
        json.dump(data, f)


def clean_creds_json():
    with open('client_secrets.json', 'w') as f:
        json.dump({}, f)
