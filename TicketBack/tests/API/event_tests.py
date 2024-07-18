import random

from django.core.exceptions import ValidationError
import pytest

from applications.events.consumers import ChatConsumer
from applications.events.models import Ticket, Event, Category
from rest_framework.test import RequestsClient

from channels.testing import WebsocketCommunicator

from settings import settings

client = RequestsClient()
allowed_hosts = settings.ALLOWED_HOSTS

if len(allowed_hosts) > 0 and allowed_hosts[0] != "*":
    BASE_URL = "https://api.ticketcrush.com/api/v1"
else:
    BASE_URL = "http://128.0.0.1:8000/api/v1"



# ********************** TEST ALL GET REQUEST


@pytest.mark.django_db()
def test_get_categories(event_resource_setup):
    path = "/category"
    response = client.get(BASE_URL + path)
    results = response.json()["results"]
    assert response.status_code == 200
    assert isinstance(results, list)


@pytest.mark.django_db()
def test_get_events_from_category(event_resource_setup):
    path = "/category/1"
    response = client.get(BASE_URL + path)
    results = response.json()['events']
    assert response.status_code == 200
    assert isinstance(results, list)


@pytest.mark.django_db()
@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_get_events(event_resource_setup):
    path = "/event"
    response = client.get(BASE_URL + path)
    results = response.json()['results']
    assert response.status_code == 200
    assert isinstance(results, list)


@pytest.mark.django_db()
@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_get_tickets_from_event(event_resource_setup):
    slug = Event.objects.get(id=1).slug
    path = f"/event/{slug}"
    response = client.get(BASE_URL + path)
    results = response.json()
    assert response.status_code == 200
    assert results['tickets']['count'] >= 1


@pytest.mark.django_db()
@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_get_prize_from_event(event_resource_setup):
    path = "/prize/1"
    response = client.get(BASE_URL + path)
    results = response.json()
    assert response.status_code == 200
    assert "id" in results


@pytest.mark.django_db()
@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_get_one_ticket_from_event(event_resource_setup):
    uuid = Ticket.objects.first()
    path = f"/ticket/{uuid.uuid}"
    response = client.get(BASE_URL + path)
    results = response.json()
    assert response.status_code == 200
    assert "uuid" in results


@pytest.mark.skip
@pytest.mark.django_db()
@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_get_all_winner_tickets_from_event(event_resource_setup):
    """
    NOTE: default (in this fixture) all tickets are not winner
    """
    path = f"/winners/"
    response = client.get(BASE_URL + path)
    results = response.json()

    # list will be empty, because all tickets are not winner
    assert response.status_code == 200
    assert results['count'] == 0

    ticket = Ticket.objects.first()
    ticket.is_winner = True
    ticket.save()
    response = client.get(BASE_URL + path)
    results = response.json()

    # after in event appeared winner ticket
    assert response.status_code == 200
    assert results['count'] == 1


@pytest.mark.django_db()
@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_get_agr_home(event_resource_setup):
    path = f"/agr/home/"
    response = client.get(BASE_URL + path)
    results = response.json()

    assert response.status_code == 200
    assert results['events'] and results['categories']
    assert len(results['events']) <= 6
    assert len(results['categories']) == len(Category.objects.all())


# ********************* OTHER FUNCTIONAL TESTS

@pytest.mark.django_db()
@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_add_tickets_to_event_with_same_number(event_resource_setup):
    event = Event.objects.get(id=1)

    with pytest.raises(ValidationError) as e:
        for r in range(2):
            Ticket.objects.create(
                event=event,
                number=1000,
                price=100,
            )


@pytest.mark.django_db()
@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_add_tickets_in_different_event_with_same_number(event_resource_setup):
    event_1 = Event.objects.get(id=1)
    event_2 = Event.objects.get(id=2)

    for event in [event_1, event_2]:
        Ticket.objects.create(
            event=event,
            number=1000,
            price=100,
        )

    assert Ticket.objects.filter(number=1000).count() == 2


# ********************* TEST PAGINATION

@pytest.mark.django_db()
@pytest.mark.filterwarnings('ignore::RuntimeWarning')
@pytest.mark.parametrize("path", ("/category", "/event"))
def test_pagination_to_get_categoties_and_event(path, event_resource_setup):

    response = client.get(BASE_URL + path)
    next = response.json()["next"]
    previous = response.json()["previous"]

    while next is not None:
        response = client.get(next)
        next = response.json()["next"]
        previous = response.json()["previous"]
        assert response.status_code == 200

    while previous is not None:
        response = client.get(previous)
        previous = response.json()["previous"]
        assert response.status_code == 200


@pytest.mark.django_db()
@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_ticket_pagination(event_resource_setup):
    event = Event.objects.get(id=2)

    for record in range(20):
        Ticket.objects.create(
            event=event,
            number=record,
            price=100,
        )
    response = client.get(BASE_URL + '/event/' + f'{event.slug}/' + '?page_size=2')
    next = response.json()['tickets']['next']
    previous = response.json()['tickets']['previous']

    # scroll tickets forward
    while next is not None:
        response = client.get(next)
        next = response.json()['tickets']["next"]
        previous = response.json()['tickets']["previous"]
        assert response.status_code == 200

    # scroll tickets back
    while previous is not None:
        response = client.get(previous)
        previous = response.json()['tickets']["previous"]
        assert response.status_code == 200


@pytest.mark.django_db()
@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_ticket_pagination_page_parameter(event_resource_setup):
    event = Event.objects.get(id=2)

    for record in range(10):
        Ticket.objects.create(
            event=event,
            number=record,
            price=100,
        )

    response = client.get(BASE_URL + '/event/' + f'{event.slug}/?page_size=5')
    next = response.json()['tickets']['next']

    if next:
        response = client.get(BASE_URL + '/event/' + f'{event.slug}/?page_size=5&page=2')
        assert response.status_code == 200

    # incorrect page
    response = client.get(BASE_URL + '/event/' + f'{event.slug}/?page=1000')
    assert response.status_code == 404


@pytest.mark.django_db()
@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_ticket_pagination_page_size_parameter(event_resource_setup):
    event = Event.objects.get(id=2)
    for record in range(20):
        Ticket.objects.create(
            event=event,
            number=record,
            price=100,
        )
    random_pack_of_tickets = random.randint(1, 19)
    response = client.get(BASE_URL + '/event/' + f'{event.slug}/' + f'?page_size={random_pack_of_tickets}')
    assert response.json()['tickets']['page_tickets_count'] == random_pack_of_tickets
    assert response.status_code == 200


# ******************* TEST FILTERS

@pytest.mark.django_db()
@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_tickets_filter_status(event_resource_setup):
    '''
    NOTE: by default, tickets are created with an open status
    '''
    event = Event.objects.get(id=2)

    for record in range(10):
        Ticket.objects.create(
            event=event,
            number=record,
            price=100,
        )

    response = client.get(BASE_URL + '/event/' + event.slug + '?status=open')
    assert response.json()['tickets']['count'] == 10

    response = client.get(BASE_URL + '/event/' + event.slug + '?status=sold')
    assert response.json()['tickets']['count'] == 0


@pytest.mark.django_db()
@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def test_tickets_filter_numbers(event_resource_setup):
    event = Event.objects.get(id=2)

    for record in range(10):
        Ticket.objects.create(
            event=event,
            number=record,
            price=100,
        )

    # select one ticket
    random_number_of_tickets = random.randint(1, 9)
    response = client.get(BASE_URL + '/event/' + event.slug + f'?numbers={random_number_of_tickets}')
    assert response.json()['tickets']['count'] == 1

    # select pack of tickets
    response = client.get(BASE_URL + '/event/' + event.slug + '?numbers=1,2,3,4')
    assert response.json()['tickets']['count'] == 4


# ******************** TEST SOCKETS

@pytest.mark.asyncio
@pytest.mark.django_db()
@pytest.mark.filterwarnings('ignore::RuntimeWarning')
async def test_connect_consumer():
    communicator = WebsocketCommunicator(ChatConsumer(), "/ws/connection/")
    connected, _ = await communicator.connect()
    assert connected


@pytest.mark.parametrize('channel', ['event', 'ticket', 'order'])
@pytest.mark.asyncio
@pytest.mark.django_db()
@pytest.mark.filterwarnings('ignore::RuntimeWarning')
async def test_subscribe_to_channels_and_get_response(channel):
    communicator = WebsocketCommunicator(ChatConsumer(), "/ws/connection/")
    connected, _ = await communicator.connect()

    await communicator.send_json_to(
        {
            "action": "send",
            "request_id": "624ca49d-8943-4609-8430-76847c72176a",
            "method": "s",
            "params": {"channel": f"{channel}"}
        }
    )

    response = await communicator.receive_json_from()

    assert response == {
        "message": {
            "channel": f"{channel}",
            "data": {
                "type": "s",
                "body": 'null',
                "request_id": "624ca49d-8943-4609-8430-76847c72176a",
            },
            "status": 200
        }
    }

    await communicator.disconnect()
