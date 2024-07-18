from django.conf import settings
from django.http import Http404

from applications.sales.models import PaymentTokenService
from applications.users.models import CustomUser as User
from applications.users.services import get_user_by_token


def user_get_me(*, user: User, jwt=None):

    token = PaymentTokenService.objects.filter(user=user).first()
    json = {'status': 'exists', 'card_last_digits': token.last_digits} if token else False

    data = {
        'id': user.id,
        'email': user.email,
        'image': user.image,
        'payment_token': json,
    }

    if jwt:
        jwt['user'] = data
        return jwt

    return data


def get_first_matching_attr(obj, *attrs, default=None):
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)

    return default


def get_error_message(exc) -> str:
    if hasattr(exc, 'message_dict'):
        return exc.message_dict
    error_msg = get_first_matching_attr(exc, 'message', 'messages')

    if isinstance(error_msg, list):
        error_msg = ', '.join(error_msg)

    if error_msg is None:
        error_msg = str(exc)

    return error_msg


def is_authenticate(request):
    use_hide = settings.USE_HIDE
    if use_hide:
        auth_token = request.headers.get('Authorization')
        if auth_token:
            user = get_user_by_token(auth_token.split(' ')[1])
            if user:
                return user
        raise Http404('Page not found')
