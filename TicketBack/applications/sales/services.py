
from rest_framework import status
from rest_framework.response import Response

from applications.sales.models import Order, PaymentTokenService
from applications.users.services import renew_user, record_payment_token


def update_order(
        order_list,
        serializer,
) -> None:

    order_list.update(
        name=serializer.validated_data.get('name'),
        email=serializer.validated_data.get('email'),
        phone=serializer.validated_data.get('phone'),
    )


def service_auth_user(
        request,
        serializer,
        response,
        user,
):
    if user:
        renew_user(user, serializer)
        if str(request.GET.get('save-card')).lower() == 'true':
            record_payment_token(user, response['customer_reply']['payment_token'], serializer)


def send_mail(order):
    try:
        Order.objects.get(uuid=order.uuid).mail_client()
    except Exception as e:
        return Response({'error': f'smtp-server: {e}'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'status': 200, 'answer': 'Operation successful'}, status=status.HTTP_200_OK)
