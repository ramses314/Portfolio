import datetime
import time
import pytest
from django.utils import timezone

from applications.events.models import Event, Category
from rest_framework.test import RequestsClient

from applications.sales.models import Order
from settings import settings

client = RequestsClient()
allowed_hosts = settings.ALLOWED_HOSTS

if len(allowed_hosts) > 0 and allowed_hosts[0] != '*':
    BASE_URL = 'https://api.ticketcrush.com/api/v1'
else:
    BASE_URL = 'http://128.0.0.1:8000/api/v1'


@pytest.mark.django_db()
def test_connect_to_scheduler(cron_setup):
    """
    Scheduler creates tasks at trigger points and the time
    after which they should be executed in the background
    """
    scheduler = cron_setup
    assert str(type(scheduler)) == "<class 'apscheduler.schedulers.background.BackgroundScheduler'>"


@pytest.mark.django_db()
def test_jobs_event_date_is_expired(cron_setup):
    """
     NOTE: formation of the jobs_id : << event_expired_{{event.id}} >>
     While time.sleep(2 seconds) job was complited after 1 second (list of jobs - 1)
    """
    scheduler = cron_setup

    Event.objects.create(
        title=f'Horse racing',
        expired= timezone.now() + datetime.timedelta(seconds=1),
        category=Category.objects.create(title=f'Racing'),
    )
    assert len(scheduler.get_jobs()) == 1

    time.sleep(2)

    assert len(scheduler.get_jobs()) == 0


@pytest.mark.django_db()
def test_jobs_event_expired_after_update(cron_setup, sales_resource_setup):
    """
     NOTE: the task is set when creating an order,
      and when updating, it is overwritten
    """
    scheduler = cron_setup
    scheduler.remove_all_jobs()
    jobs_before = [i.name for i in scheduler.get_jobs()]

    event = Event.objects.get(id=1)
    event.title = 'New_title'
    event.save()

    jobs_after = [i.name for i in scheduler.get_jobs()]

    assert len(jobs_after) - len(jobs_before) == 1
    assert 'jobs_event_date_expired' not in jobs_before
    assert 'jobs_event_date_expired' in jobs_after


@pytest.mark.skip(reason="for dev ...")
@pytest.mark.django_db()
def test_jobs_order_expired(cron_setup):
    scheduler = cron_setup
    jobs_before = [i.name for i in scheduler.get_jobs()]
    Order.objects.create(
        user_uuid='45804280983'
    )
    jobs_after = [i.name for i in scheduler.get_jobs()]

    assert len(jobs_after) - len(jobs_before) == 1
    assert 'jobs_order_expired' not in jobs_before
    assert 'jobs_order_expired' in jobs_after
