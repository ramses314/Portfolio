import datetime
import time

from django import http
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, serializers
from .models import Category, Event, Ticket
from . import mixins as event_mixins
from .utils import EventPagination
from ..users.utils import is_authenticate


class CategoryViewSet(
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet,
):
    """
    return list categories or category
    """

    model = models.Category

    def get_queryset(self):
        is_authenticate(self.request)
        return self.model.published.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.CategoryDetailSerializer
        if self.action == 'list':
            return serializers.CategoryListSerializer
        return super().get_serializer_class()


class EventViewSet(
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        event_mixins.EventQuerysetMixin,
        viewsets.GenericViewSet,
):
    """
    return list events or event
    """

    model = models.Event
    lookup_field = 'slug'
    pagination = 10

    def get_serializer_class(self):
        is_authenticate(self.request)
        if self.action == 'retrieve':
            return serializers.EventDetailSerializer
        if self.action == 'list':
            return serializers.EventListSerializer
        return super().get_serializer_class()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        time.sleep(0.5)
        return Response(data)


class EventWinnersViewSet(
        mixins.ListModelMixin,
        viewsets.GenericViewSet,
):
    """
    return list events or event
    """

    model = models.Event
    lookup_field = 'slug'
    serializer_class = serializers.EventWinnersListSerializer
    pagination_class = EventPagination

    def get_queryset(self):
        is_authenticate(self.request)
        return self.model.published.filter(tickets__is_winner=True).distinct().order_by('-expired')

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request, view=self)

        if paginated_queryset is not None:
            serializer = self.get_serializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response([])


class AgrHomeViewSet(viewsets.ViewSet):

    def list(self, request):
        is_authenticate(request)
        events = Event.objects.all()[:6]
        categories = Category.objects.all()
        serializer_event = serializers.EventListSerializer(data=events, context={'request': request}, many=True)
        serializer_category = serializers.CategoryListSerializer(data=categories, many=True)
        serializer_event.is_valid()
        serializer_category.is_valid()

        response = {
            'events': serializer_event.data,
            'categories': serializer_category.data,
        }
        return Response(response)


class TicketViewSet(
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet,
):
    """
    return list ticket or 404
    """

    model = models.Ticket
    serializer_class = serializers.TicketDetailSerializer

    def get_queryset(self):
        is_authenticate(self.request)
        ticket = models.Ticket.objects.filter(uuid=self.kwargs.get('pk')).first()
        if ticket:
            return models.Event.published.filter(id=ticket.event.id).first().tickets.all()
        raise http.Http404()


class PrizeViewSet(
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet,
):
    """
    return list prize or 404
    """

    model = models.Prize
    serializer_class = serializers.PrizeDetailSerializer

    def get_queryset(self):
        is_authenticate(self.request)
        prize = models.Prize.objects.filter(id=self.kwargs.get('pk')).first()
        if prize:
            return models.Event.published.filter(id=prize.event.id).first().prizes.all()
        raise http.Http404()


class AdminEventChangeViewSet(APIView):

    def post(self, request, *args, **kwargs):
        from jobs.jobs import jobs_order_expired
        from applications.main.apps import MainConfig
        scheduler = MainConfig.scheduler
        jobs = [i.name for i in scheduler.get_jobs()]

        while 'fill_events' in jobs:
            time.sleep(0.5)
            jobs = [i.name for i in scheduler.get_jobs()]
        else:
            scheduler.add_job(
                jobs_order_expired,
                'date',
                run_date=datetime.datetime.now() + datetime.timedelta(days=15),
                id=f'fill_events',
                name='fill_events'
            )
            data = request.data
            event = Event.objects.filter(slug=data['slug']).first()
            last_number = event.ticket_quantity
            amount = int(data['amount'])
            price = float(data['price'])
            ticket_list = []

            for i in range(last_number, last_number + amount):
                ticket = Ticket(
                    event=event,
                    number=i + 1,
                    price=price,
                )
                ticket_list.append(ticket)
        try:
            Ticket.objects.bulk_create(ticket_list)
            event.ticket_quantity = event.ticket_quantity + amount
            event.save()
        except:
            pass
        scheduler.remove_job('fill_events')
        return Response({
            'amount': amount,
            'total': event.ticket_quantity,
        })
