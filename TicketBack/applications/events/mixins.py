from rest_framework import pagination

from . import models


class GetPPCMixin:

    def get_prizes(self, obj):
        from .serializers import PrizeDetailSerializer

        prizes = obj.prizes.all()
        paginator = pagination.PageNumberPagination()
        paginator.page_query_param = 'track_page'
        paginator.page_size_query_param = 'track_page_size'
        page = paginator.paginate_queryset(
            prizes,
            self.context['request'],
        )
        serializer = PrizeDetailSerializer(
            page,
            many=True,
            context={'request': self.context['request']},
        )
        return paginator.get_paginated_response(serializer.data).data

    def get_price(self, obj):
        if obj.price == 0 and hasattr(obj, 'tickets'):
            ticket = obj.tickets.first()
            if hasattr(ticket, 'price'):
                obj.price = ticket.price
                obj.save()
        return str(obj.price)

    def get_counter(self, obj):
        count = obj.tickets.filter(status='open').count()
        if obj.counter == 0:
            obj.counter = count
            obj.save()
        return count


class GetTicketsMixin:

    def get_tickets(self, obj):
        from .serializers import TicketDetailSerializer
        from .utils import CustomPagination

        if self.__class__.__name__ != 'EventWinnersListSerializer':
            tickets = obj.tickets.all().order_by('number')
        else:
            tickets = obj.tickets.all().filter(is_winner=True).order_by('number')

        numbers = self.context['request'].GET.get('numbers', ',').split(',')
        status = self.context['request'].GET.get('status', None)

        if status:
            tickets = tickets.filter(status=status)

        if numbers:
            try:
                tickets = tickets.filter(number__in=[int(x) for x in numbers])
            except Exception:
                pass

        paginator = CustomPagination()
        paginator.page_query_param = 'page'
        paginator.page_size_query_param = 'page_size'
        page = paginator.paginate_queryset(tickets, self.context['request'])
        serializer = TicketDetailSerializer(
            page, many=True, context={'request': self.context['request']})
        return paginator.get_paginated_response(serializer.data).data


class EventQuerysetMixin:

    def get_queryset(self):
        import datetime

        from django.db import models as dj_models

        on_landing = self.request.GET.get('on_landing')
        opened = self.request.GET.get('opened')
        closed = self.request.GET.get('closed')
        price = self.request.GET.get('price')
        counter = self.request.GET.get('counter')
        categories = self.request.GET.get('categories', ',').split(',')
        model = self.model.published.all().annotate(
            relevance=dj_models.Case(
                dj_models.When(expired__gte=datetime.datetime.now(), then=1),
                dj_models.When(expired__lt=datetime.datetime.now(), then=2),
                output_field=dj_models.IntegerField(),
            ),
        ).annotate(
            timediff=dj_models.Case(
                dj_models.When(
                    expired__gte=datetime.datetime.now(),
                    then=dj_models.F('expired') - datetime.datetime.now()),
                dj_models.When(
                    expired__lt=datetime.datetime.now(),
                    then=datetime.datetime.now() - dj_models.F('expired'),
                ),
                output_field=dj_models.DurationField(),
            ),
        ).order_by('relevance', 'timediff')
        if on_landing and str(on_landing).lower() == 'true':
            model = model.filter(on_landing=True)
        if opened and str(opened).lower() == 'true':
            model = model.filter(expired__gt=datetime.datetime.now())
        if closed and str(closed).lower() == 'true':
            model = model.filter(expired__lt=datetime.datetime.now())
        if categories:
            categories = models.Category.objects.filter(title__in=categories)
            if categories:
                model = model.filter(category__in=categories).order_by('expired')
        if price and str(price).lower() == 'true':
            model = model.order_by('-price')
        if counter and str(counter).lower() == 'true':
            model = model.order_by('-counter')
        return model
