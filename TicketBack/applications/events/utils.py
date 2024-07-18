import datetime

from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.db.models.functions import ExtractMonth, ExtractYear
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page_tickets_count': len(data),
            'next_page': self.page.number + 1 if self.page.number != self.page.paginator.num_pages else None,
            'previous_page': self.page.number - 1 if self.page.number != 1 else None,
            'results': data,
        })


def filter_queryset_by_year_and_month(queryset, year_month_map):
    q_objects = Q()

    for year, months in year_month_map.items():
        month_filters = Q()
        for month in months:
            month_filters |= Q(year=year, month=month)
        q_objects |= month_filters

    return queryset.filter(q_objects)


class EventPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    page_query_param = 'event_page'
    max_page_size = 200

    month = None
    month_quan = None
    year = None
    left_extreme = None
    right_extreme = None

    def paginate_queryset(self, queryset, request, view=None):
        queryset = queryset.annotate(month=ExtractMonth('expired'), year=ExtractYear('expired'))
        date = request.query_params.get('month', None)
        quantity = request.query_params.get('month_quan', 1)

        self.left_extreme = queryset.order_by('expired').first().expired if queryset else datetime.datetime.now()
        self.right_extreme = queryset.order_by('-expired').first().expired if queryset else datetime.datetime.now()

        if date and len(date) == 6 and str(date).isdigit() and date[:2] != '00':
            month = int(date[:2].lstrip('0'))
            month = month if 0 < month < 13 else 1
            year = int(date[2:])
        else:
            month = datetime.datetime.now().month
            year = datetime.datetime.now().year

        month_quan = int(quantity) if str(quantity).isdigit() and int(quantity) <= 12 else 1
        date = datetime.datetime(year, month, 1)
        now = datetime.datetime.now()

        if date >= datetime.datetime(now.year, now.month, 1) and month_quan != 1:
            month = datetime.datetime.now().month
            year = datetime.datetime.now().year
            date = datetime.datetime(year, month, 1)

        new_date = date - relativedelta(months=month_quan)
        new_year = new_date.year

        if new_year == year:
            month_set = [month - i for i in range(month_quan)]
            year_month_map = {year: month_set}
        else:
            month_set = [month - i for i in range(month_quan)]
            keys = month_set.index(1)
            new_month_set = [12 - i for i in range(len(month_set[keys + 1:]))]
            year_month_map = {year: month_set[:keys + 1], new_year: new_month_set}

        queryset = filter_queryset_by_year_and_month(queryset, year_month_map)
        queryset = queryset.order_by('-expired')
        self.year = year
        self.month = month
        self.month_quan = month_quan
        return super().paginate_queryset(queryset, request, view)

    def get_next_link(self):
        month_now, year_now = datetime.datetime.now().month, datetime.datetime.now().year
        if (month_now - 1 < self.month and year_now == self.year) or year_now < self.year:
            return None

        month, year, month_quan = self.month, self.year, self.month_quan
        month_quan = self.month_quan if self.month_quan else 1
        date = datetime.datetime(year, month, 1)
        new_date = date + relativedelta(months=month_quan)
        new_month = new_date.month
        new_year = new_date.year
        new_month = '0' + str(new_month) if len(str(new_month)) == 1 else new_month
        return self._get_link(new_year, new_month, month_quan)

    def get_previous_link(self):
        month_now, year_now, month_quan = datetime.datetime.now().month, datetime.datetime.now().year, self.month_quan
        date = datetime.datetime(self.year, self.month, 1)
        new_date = date - relativedelta(months=month_quan)
        date_old = datetime.datetime(self.left_extreme.year, self.left_extreme.month, 1)

        if (month_now < self.month and year_now <= self.year) or year_now < self.year or new_date < date_old:
            next_link = self.get_next_link()
            if next_link is None and new_date > datetime.datetime.now():
                pass
            else:
                return None

        month, year, month_quan = self.month, self.year, self.month_quan
        date = datetime.datetime(year, month, 1)
        new_date = date - relativedelta(months=month_quan)
        new_month = new_date.month
        new_year = new_date.year
        new_month = '0' + str(new_month) if len(str(new_month)) == 1 else new_month
        return self._get_link(new_year, new_month, month_quan)

    def _get_link(self, year, month, month_quan):
        base_url = str(self.request.build_absolute_uri()).split('?')[0]
        query_params = self.request.query_params.copy()
        query_params.pop('month', None)
        query_params.pop('month_quan', None)
        query_params['month'] = f'{month}' + f'{year}' if month else None
        query_params['month_quan'] = month_quan if month_quan else None
        encoded_params = query_params.urlencode()
        return f'{base_url}?{encoded_params}'

    def get_paginated_response(self, data):
        month, year, month_quan = self.month, self.year, self.month_quan
        month_quan = self.month_quan if self.month_quan else 1
        date = datetime.datetime(year, month, 1) + relativedelta(months=1)
        new_date = date - relativedelta(months=month_quan)
        new_month = new_date.month
        new_year = new_date.year
        new_month = '0' + str(new_month) if len(str(new_month)) == 1 else new_month
        month = '0' + str(date.month) if len(str(date.month)) == 1 else date.month
        response = super().get_paginated_response(data)
        monthly_period = f'01.{new_month}.{new_year}' + '-' + f'01.{month}.{date.year}'
        new_response = {
            'count': response.data['count'],
            'next': response.data['next'],
            'previous': response.data['previous'],
            'monthly_period': monthly_period,
            'results': response.data['results'],
        }
        response.data = new_response
        return response


def event_all_fields():

    fields = [
        'title',
        'slug',
        'on_landing',
        'content',
        'expired',
        'image',
        'ticket_quantity',
        'link',
        'time_event',
        'category',
    ]

    return fields


def renew_jobs_order_expired(scheduler, job_func, order):
    try:
        scheduler.remove_job(job_id=f'order_expired_{order.uuid}')
    except Exception as e:
        pass
    finally:
        start_date = datetime.datetime.now() + datetime.timedelta(minutes=15)
        scheduler.add_job(
            job_func,
            'date',
            run_date=start_date,
            id=f'order_expired_{order.uuid}',
            kwargs={'order': order}
        )


def remove_jobs_try(scheduler, id):
    try:
        scheduler.remove_job(job_id=id)
    except Exception as e:
        pass
