
import mercadopago

from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import MercadoPago
from .services import update_order, send_mail
from ..core.jsons import json_winner_response
from ..events.models import Order, Ticket
from ..events.utils import remove_jobs_try
from . import serializers

from applications.main.apps import MainConfig
from ..users.utils import is_authenticate


class OrderViewSet(viewsets.ModelViewSet):
    '''
    return order of user
    '''

    model = Order
    serializer_class = serializers.OrderSerializer
    queryset = ''

    def get_object(self) -> Order:
        serializer: serializers.OrderGetSerializer = serializers.OrderGetSerializer(
            data={'uuid': self.kwargs.get('pk')})
        serializer.is_valid(raise_exception=True)
        return get_object_or_404(Order, uuid=serializer.validated_data.get('uuid'))

    @staticmethod
    def save_ticket(ticket: Ticket, order: Order, method: str) -> Response:
        status_save = ticket.Status.BLOCKED if method == 'add' else ticket.Status.OPEN
        order_save = order if method == 'add' else None
        ticket.order = order_save
        ticket.status = status_save
        ticket.save()
        return Response(serializers.OrderSerializer(order).data, status=status.HTTP_200_OK)

    @action(
        methods=['post'],
        detail=False,
        url_path='add_product',
    )
    def add_product(self, request) -> Response:
        is_authenticate(request)
        serializer: serializers.AddProductSerializer = serializers.AddProductSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        ticket = Ticket.objects.get(uuid=serializer.validated_data.get('ticket_uuid'))
        order, _ = Order.opened.get_or_create(user_uuid=serializer.validated_data.get('user_uuid'))
        return self.save_ticket(ticket, order, 'add')

    @action(
        methods=['post'],
        detail=False,
        url_path='delete_product',
    )
    def delete_product(self, request) -> Response:
        is_authenticate(request)
        serializer: serializers.DeleteProductSerializer = serializers.DeleteProductSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        order = Order.objects.filter(
            uuid=serializer.validated_data.get('order_uuid'),
            user_uuid=serializer.validated_data.get('user_uuid')).first()
        ticket = order.tickets.only('status', 'order', 'qr_code')\
            .filter(uuid=serializer.validated_data.get('ticket_uuid')).first()
        return self.save_ticket(ticket, order, 'delete')

    @action(
        methods=['post'],
        detail=False,
        url_path='send_order',
    )
    def send_order(self, request):
        user = is_authenticate(request)
        serializer = serializers.UpdateTokenOrderSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        order_list = Order.opened.filter(user_uuid=serializer.validated_data.get('user_uuid'))
        order = order_list.first()
        mp = MercadoPago.objects.first()

        payment_data = {
            "transaction_amount": float(order.amount),
            "token": serializer.validated_data.get('card_token'),
            "installments": 1,
            "payment_method_id": serializer.validated_data.get('payment_method_id'),
            "payer": {
                "email": serializer.validated_data.get('email'),
                "identification": {
                    "type": "RFC",
                    "number": "ABCD123456EFG"
                }
            }
        }

        payment_response = mercadopago.SDK(mp.access_token).payment().create(payment_data)
        payment = payment_response["response"]

        if payment and payment['status'] != 'approved':
            Order.objects.filter(uuid=order.uuid).update(status=Order.Status.WAITING)
            error_message = payment['message'] if 'message' in payment else 'payment rejected'
            return Response({
                    'status': 400,
                    'message': f'Operation failed: {error_message}'
                })

        update_order(order_list, serializer)
        Order.objects.filter(uuid=order.uuid).update(
            status=Order.Status.PAYED,
            user_uuid=user.username,
            condition=Order.Condition.READ,
            add_hash=None
        )
        order.tickets.update(status=Ticket.Status.SOLD)
        remove_jobs_try(MainConfig.scheduler, f'order_expired_{order.uuid}')
        return send_mail(order)

    @action(
        methods=['post'],
        detail=False,
        url_path='winner',
    )
    def winner(self, request) -> Response:
        is_authenticate(request)
        serializer: serializers.OrderGetSerializer = serializers.OrderGetSerializer(
            data={'uuid': request.data.get('uuid')})
        serializer.is_valid(raise_exception=True)
        order = Order.objects.prefetch_related('tickets', 'tickets__event', 'tickets__event__prizes').only('uuid').\
            get(uuid=serializer.validated_data.get('uuid'))
        tickets = order.tickets.all()
        events = list(set([i.event for i in tickets]))
        order_json = serializers.OrderSerializer(order).data
        del order_json['tickets']
        order_json['order_events'] = []
        order_json = order_json if events else {'status': 'Order is empty'}

        for event in events:
            tickets = order.tickets.filter(event_id=event.id)
            order_json['order_events'].append(json_winner_response(event, tickets))
        return Response(order_json, status=status.HTTP_200_OK)


class OrderDestroyViewSet(
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet,
):
    """
    Delete order
    """

    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def get_object(self):
        serializer: serializers.OrderGetSerializer = serializers.OrderGetSerializer(
            data={'uuid': self.kwargs.get('pk')})
        serializer.is_valid(raise_exception=True)
        order = Order.objects.get(uuid=serializer.validated_data.get('uuid'))
        self.destroy(order, self.request)

    def destroy(self, order, request, *args, **kwargs):
        if order.status == Order.Status.PAYED:
            return Response(
                {
                    'status': 400,
                    'data': {
                        'order': 'payed: cant delete'
                    }
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        self.perform_destroy(order)
        return Response(
            {
                'status': 204,
                'data': {
                    'order': 'delete'
                }
            },
            status=status.HTTP_204_NO_CONTENT,
        )
