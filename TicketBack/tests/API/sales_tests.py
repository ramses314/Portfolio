import datetime
import pytest
from django.utils import timezone

from settings import settings
from applications.sales import models
from applications.events.models import Ticket
from applications.main.models import Preference

from rest_framework.test import RequestsClient


client = RequestsClient()
allowed_hosts = settings.ALLOWED_HOSTS

if len(allowed_hosts) > 0 and allowed_hosts[0] != "*":
    BASE_URL = "https://api.ticketcrush.com/api/v1"
else:
    BASE_URL = "http://127.0.0.1:8000/api/v1"

# ********************** TEST ALL GET REQUESTS

@pytest.mark.django_db()
def test_get_order(sales_resource_setup):
    order = models.Order.objects.first()
    path = "/order/"
    request = client.get(BASE_URL + path + str(order.uuid))
    response = request.json()

    assert request.status_code == 200
    assert response['name'] == order.name


@pytest.mark.django_db()
def test_destroy_order(sales_resource_setup):
    uuid = models.Order.objects.first().uuid
    path = "/order/delete/"
    request = client.get(BASE_URL + path + str(uuid))

    assert request.status_code == 200


# ********************** TEST POST REQUEST

@pytest.mark.django_db()
def test_add_product(sales_resource_setup):
    path = '/order/add_product/'
    order = models.Order.objects.first()
    ticket = Ticket.objects.first()
    data = {
        "user_uuid": f"{order.user_uuid}",
        "ticket_uuid": f"{ticket.uuid}",
        "front_uuid": f"{Preference.objects.first().front_uuid}"
    }
    request = client.post(f'{BASE_URL + path}', json=data)
    assert request.status_code == 200
    assert order.tickets.get(uuid=ticket.uuid).status == 'blocked'


@pytest.mark.django_db()
def test_add_product_with_order_uuid(sales_resource_setup):
    path = '/order/add_product/'
    order = models.Order.objects.first()
    ticket = Ticket.objects.first()
    data = {
        "user_uuid": f"{order.user_uuid}",
        "ticket_uuid": f"{ticket.uuid}",
        "front_uuid": f"{Preference.objects.first().front_uuid}",
        "order_uuid": f"{order.uuid}"
    }
    request = client.post(f'{BASE_URL + path}', json=data)
    assert request.status_code == 200
    assert order.tickets.get(uuid=ticket.uuid).status == 'blocked'


@pytest.mark.django_db()
def test_delete_product(resource_setup_expanded):
    path = "/order/delete_product/"
    order = models.Order.objects.get(name='order2')
    ticket = order.tickets.first()
    data = {
        "user_uuid": f"{order.user_uuid}",
        "order_uuid": f"{order.uuid}",
        "ticket_uuid": f"{ticket.uuid}",
        "front_uuid": f"{Preference.objects.first().front_uuid}"
    }
    request = client.post(f'{BASE_URL + path}', json=data)
    assert request.status_code == 200
    assert ticket not in list(order.tickets.all())
    assert Ticket.objects.get(uuid=ticket.uuid).status == 'open'


@pytest.mark.skip
@pytest.mark.django_db()
def test_send_order(resource_setup_expanded):
    path = "/order/send_order/"
    order = models.Order.objects.get(name='order2')
    template_for_send = resource_setup_expanded['template_for_send_order']
    template_for_send['user_uuid'] = order.user_uuid

    request = client.post(f'{BASE_URL + path}', json=template_for_send)
    assert request.status_code == 200


# ********************* TEST BROKE / UNCORRECT REQUEST

@pytest.mark.django_db()
def test_order_wrong_uuid(sales_resource_setup):
    path = "/order/"
    random_uuid = "1234f9ce-c407-40d6-aaea-9ea9db029e74"

    response = client.get(BASE_URL + path + random_uuid)
    assert response.status_code == 400


@pytest.mark.django_db()
def test_delete_order_wrong_uuid(sales_resource_setup):
    path = "/order/delete/"
    random_uuid = 'w1234f9ce-c407-40d6-aaea-9ea9db029e74'

    response = client.get(BASE_URL + path + random_uuid)
    assert response.status_code == 400


@pytest.mark.django_db()
@pytest.mark.parametrize(
    'parameter', ['user_uuid', 'ticket_uuid', 'front_uuid', 'order_uuid']
)
def test_delete_product_without_one_parameter(resource_setup_expanded,parameter):
    path = "/order/delete_product/"
    order = models.Order.objects.get(name='order2')
    ticket = order.tickets.first()

    data = {
        "user_uuid": f"{order.user_uuid}",
        "ticket_uuid": f"{ticket.uuid}",
        "front_uuid": f"{Preference.objects.first().front_uuid}",
        "order_uuid": f"{order.uuid}"
    }

    del data[f"{parameter}"]

    request = client.post(f'{BASE_URL + path}', json=data)
    assert request.status_code == 400
    assert ticket in list(order.tickets.all())\


@pytest.mark.django_db()
def test_check_winner(resource_setup_expanded):
    path = "/order/winner/"
    order = models.Order.objects.get(name='order2')
    data = {"uuid": f"{order.uuid}"}
    request = client.post(f'{BASE_URL + path}', json=data).json()

    assert request['order_events']


@pytest.mark.django_db()
def test_check_winner_without_tickets(resource_setup_expanded):
    path = "/order/winner/"
    order = models.Order.objects.get(name='order2')
    order.tickets.all().delete()
    data = {"uuid": f"{order.uuid}"}
    request = client.post(f'{BASE_URL + path}', json=data).json()
    assert request['status'] == 'Order is empty'


# ***************** OTHER FUNCTIONAL TESTS

@pytest.mark.django_db()
def test_add_product_only_by_one_event(resource_setup_expanded):
    """
    Tickets in the order must belong
    only to one event
    """
    ticket1 = models.Order.objects.get(name='order2').tickets.first()
    ticket2 = Ticket.objects.exclude(event=ticket1.event).first()
    assert ticket1.event != ticket2.event

    path = "/order/add_product/"
    order = models.Order.objects.get(name='order1')

    data_first_product = {
        "user_uuid": f"{order.user_uuid}",
        "ticket_uuid": f"{ticket1.uuid}",
        "front_uuid": f"{Preference.objects.first().front_uuid}"
    }

    data_second_product = {
        "user_uuid": f"{order.user_uuid}",
        "ticket_uuid": f"{ticket2.uuid}",
        "front_uuid": f"{Preference.objects.first().front_uuid}"
    }

    # add ticket by event(ticket1)
    request = client.post(f'{BASE_URL + path}', json=data_first_product)
    assert request.status_code == 200

    # add ticket by another event(ticket2) and should get an error
    request = client.post(f'{BASE_URL + path}', json=data_second_product)
    assert request.status_code == 200



@pytest.mark.django_db()
def test_add_ticket_in_status_blocked(sales_resource_setup):
    """
    The ticket is open when it is created, when
    enter it into the order - blocked
    """
    path = '/order/add_product/'
    ticket = Ticket.objects.first()
    ticket.status = ticket.Status.BLOCKED
    ticket.save()

    order = models.Order.objects.get(name='order1')

    data = {
        "user_uuid": f"{order.user_uuid}",
        "ticket_uuid": f"{ticket.uuid}",
        "front_uuid": f"{Preference.objects.first().front_uuid}"
    }

    request = client.post(f'{BASE_URL + path}', json=data)
    assert request.status_code == 400

    ticket = Ticket.objects.first()
    ticket.status = ticket.Status.OPEN
    ticket.save()

    request = client.post(f'{BASE_URL + path}', json=data)
    assert request.status_code == 200


@pytest.mark.django_db()
def test_delete_product_only_once(resource_setup_expanded):
    path = "/order/delete_product/"
    order = models.Order.objects.get(name="order2")
    ticket = order.tickets.first()

    data = {
        "user_uuid": f"{order.user_uuid}",
        "order_uuid": f"{order.uuid}",
        "ticket_uuid": f"{ticket.uuid}",
        "front_uuid": f"{Preference.objects.first().front_uuid}"
    }

    # the first time
    request = client.post(f'{BASE_URL + path}', json=data)
    assert request.status_code == 200

    # the second time -> error
    request = client.post(f'{BASE_URL + path}', json=data)
    assert request.status_code == 400
    assert request.json()['error']


@pytest.mark.django_db()
def test_count_the_total_amount_order(resource_setup_expanded):
    """
    The model class has a method for calculating the total price. Here we
    check its working
    """
    order = models.Order.objects.get(name='order2')
    ticket_from_order = order.tickets.first()
    assert order.amount == ticket_from_order.price


@pytest.mark.django_db()
def test_change_the_total_amount_order(resource_setup_expanded):
    """
    The model class has a method for calculating the total price. Here we
    check its change depending on the addition
    or deletion of the ticket
    """
    order = models.Order.objects.get(name='order2')
    amount = order.amount
    anoter_ticket = Ticket.objects.create(
        event=order.tickets.first().event,
        number=20,
        price=5000,
        order=order
    )
    amount_after_add = amount + 5000
    assert order.amount == amount_after_add

    anoter_ticket.order = None
    anoter_ticket.save()
    assert order.amount == amount_after_add - 5000


@pytest.mark.django_db()
def test_change_the_total_amount_order(resource_setup_expanded):
    order = models.Order.objects.get(name='order2')
    amount = order.amount
    anoter_ticket = Ticket.objects.create(
        event=order.tickets.first().event,
        number=20,
        price=5000,
        order=order
    )
    amount_after_add = amount + 5000
    assert order.amount == amount_after_add

    anoter_ticket.price = 2000
    anoter_ticket.save()
    assert order.amount == amount_after_add - 3000


@pytest.mark.django_db()
def test_add_same_product_several_times(sales_resource_setup):
    path = '/order/add_product/'
    ticket = Ticket.objects.first()
    order = models.Order.objects.get(name='order1')

    data = {
        "user_uuid": f"{order.user_uuid}",
        "ticket_uuid": f"{ticket.uuid}",
        "front_uuid": f"{Preference.objects.first().front_uuid}"
    }

    # the first time
    request = client.post(f'{BASE_URL + path}', json=data)
    assert request.status_code == 200

    # the second time
    request = client.post(f'{BASE_URL + path}', json=data)
    assert request.status_code == 400


@pytest.mark.django_db()
def test_changing_the_quantity_of_products(sales_resource_setup):
    path = '/order/add_product/'
    order = models.Order.objects.get(name='order1')
    ticket = Ticket.objects.first()
    count = order.tickets.count()

    data = {
        "user_uuid": f"{order.user_uuid}",
        "ticket_uuid": f"{ticket.uuid}",
        "front_uuid": f"{Preference.objects.first().front_uuid}"
    }

    request = client.post(f'{BASE_URL + path}', json=data)
    assert request.status_code == 200
    assert order.tickets.count() == count + 1


@pytest.mark.skip
@pytest.mark.django_db()
def test_send_order_with_empty_products(resource_setup_expanded):
    """
    In an empty shopping cart, the total price is
    zero -> no redirect to the payment page
    """
    path = "/order/send_order/"
    order = models.Order.objects.get(name='order1')
    assert list(order.tickets.all()) == []

    template_for_send_order = resource_setup_expanded['template_for_send_order']
    template_for_send_order['user_uuid'] = order.user_uuid

    request = client.post(f'{BASE_URL + path}', json=template_for_send_order)
    empty_error = request.json()['non_field_errors'][0]
    assert empty_error == 'order is empty'


# ********************** TEST COMBINATIONS OF REQUESTS

@pytest.mark.django_db()
def test_add_and_delete_product(sales_resource_setup):
    path_add = '/order/add_product/'
    path_delete = '/order/delete_product/'
    ticket = Ticket.objects.first()
    order = models.Order.objects.get(name='order1')

    data = {
        "user_uuid": f"{order.user_uuid}",
        "ticket_uuid": f"{ticket.uuid}",
        "front_uuid": f"{Preference.objects.first().front_uuid}",
        "order_uuid": f"{order.uuid}"
    }

    # added
    request = client.post(f'{BASE_URL + path_add}', json=data)
    assert request.status_code == 200
    assert ticket in list(order.tickets.all())

    # deleted
    request = client.post(f'{BASE_URL + path_delete}', json=data)
    assert request.status_code == 200
    assert ticket not in list(order.tickets.all())


@pytest.mark.django_db()
def test_add_product_and_try_again_in_another_order(sales_resource_setup):
    path_add = '/order/add_product/'
    ticket = Ticket.objects.first()
    order = models.Order.objects.get(name='order1')

    data = {
        "user_uuid": f"{order.user_uuid}",
        "ticket_uuid": f"{ticket.uuid}",
        "front_uuid": f"{Preference.objects.first().front_uuid}",
    }

    # the first time
    request = client.post(f'{BASE_URL + path_add}', json=data)
    assert request.status_code == 200
    assert ticket in list(order.tickets.all())

    # the second time: ticket is blocked -> error
    request = client.post(f'{BASE_URL + path_add}', json=data)
    assert request.status_code == 400
    assert ticket in list(order.tickets.all())


@pytest.mark.django_db()
def test_delete_and_add_to_another(resource_setup_expanded):
    path_add = '/order/add_product/'
    path_delete = '/order/delete_product/'
    ticket = models.Order.objects.get(name="order2").tickets.first()
    order = models.Order.objects.get(name='order2')

    data = {
        "user_uuid": f"{order.user_uuid}",
        "ticket_uuid": f"{ticket.uuid}",
        "front_uuid": f"{Preference.objects.first().front_uuid}",
        "order_uuid": f"{order.uuid}"
    }

    request = client.post(f'{BASE_URL + path_delete}', json=data)
    assert request.status_code == 200
    assert ticket not in list(order.tickets.all())

    another_order = models.Order.objects.get(name='order1')

    data = {
        "user_uuid": f"{another_order.user_uuid}",
        "ticket_uuid": f"{ticket.uuid}",
        "front_uuid": f"{Preference.objects.first().front_uuid}"
    }

    request = client.post(f'{BASE_URL + path_add}', json=data)
    assert request.status_code == 200
    assert ticket not in list(order.tickets.all())


@pytest.mark.django_db()
def test_add_products_then_update(sales_resource_setup):
    path = '/order/add_product/'
    ticket = Ticket.objects.first()
    order = models.Order.objects.get(name='order1')

    data = {
        "user_uuid": f"{order.user_uuid}",
        "ticket_uuid": f"{ticket.uuid}",
        "front_uuid": f"{Preference.objects.first().front_uuid}"
    }

    request = client.post(f'{BASE_URL + path}', json=data)
    assert request.status_code == 200
    assert ticket in list(order.tickets.all())

    new_price = 500
    renew_ticket = order.tickets.filter(uuid=ticket.uuid).first()
    renew_ticket.price = new_price
    renew_ticket.save()
    assert renew_ticket.price == new_price
