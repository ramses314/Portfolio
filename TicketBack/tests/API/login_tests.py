import pytest

from applications.sales.models import Order
from applications.users.models import CustomUser
from settings import settings

from rest_framework.test import RequestsClient


client = RequestsClient()
allowed_hosts = settings.ALLOWED_HOSTS

if len(allowed_hosts) > 0 and allowed_hosts[0] != "*":
    BASE_URL = "https://api.ticketcrush.com/api/v1"
else:
    BASE_URL = "http://127.0.0.1:8000/api/v1"


@pytest.mark.skip
@pytest.mark.django_db()
def test_registration():
    user = {
        'email': 'root@gmail.com',
        'password1': '000000',
        'password2': '000000',

    }
    path = "/auth/registration/"
    request = client.post(BASE_URL + path, json=user)
    assert request.status_code == 201
    assert request.json()['detail'] == 'Verification e-mail sent.'


@pytest.mark.skip
@pytest.mark.django_db()
def test_login():
    CustomUser.objects.create_user(
        email='root229@gmail.com',
        password='1234'
    )

    path = "/auth/login/"
    request = client.post(BASE_URL + path, json={'email': 'root229@gmail.com', 'password': '1234'})
    response = request.json()

    assert request.status_code == 200
    assert response['access_token']
    assert response['refresh_token']
    assert response['user']


@pytest.mark.skip
@pytest.mark.django_db()
def test_access_token(login_resource_setup):

    path = "/auth/login/"
    request = client.post(BASE_URL + path, json={'email': 'root229@gmail.com', 'password': '1234'})
    response = request.json()

    access_token = response['access_token']
    path = '/auth/token/verify/'
    request = client.post(BASE_URL + path, json={'token': access_token})
    assert request.status_code == 200
    assert request.json() == {}

    # test wrong access token
    wrong_access_token = access_token[:-1]
    request = client.post(BASE_URL + path, json={'token': wrong_access_token})
    assert request.status_code == 401
    assert request.json()['detail'] == 'Token is invalid or expired'


@pytest.mark.skip
@pytest.mark.django_db()
def test_refresh_token(login_resource_setup):

    path = "/auth/login/"
    request = client.post(BASE_URL + path, json={'email': 'root229@gmail.com', 'password': '1234'})
    response = request.json()
    refresh_token = response['refresh_token']

    path = '/auth/token/refresh/'
    request = client.post(BASE_URL + path, json={'refresh': refresh_token})
    assert request.status_code == 200
    assert request.json()['access']
    assert request.json()['refresh']


@pytest.mark.skip
@pytest.mark.django_db()
def test_refresh_token_with_access(login_resource_setup):
    path = "/auth/login/"
    request = client.post(BASE_URL + path, json={'email': 'root229@gmail.com', 'password': '1234'})
    response = request.json()

    refresh_token = response['refresh_token']
    path = '/auth/token/refresh/'
    request = client.post(BASE_URL + path, json={'refresh': refresh_token})
    new_refresh_token = request.json()['access']

    path = '/auth/token/verify/'
    request = client.post(BASE_URL + path, json={'token': new_refresh_token})
    assert request.status_code == 200
    assert request.json() == {}


@pytest.mark.skip
@pytest.mark.django_db()
def test_user_profile(login_resource_setup):
    path = "/auth/login/"
    request = client.post(BASE_URL + path, json={'email': 'root229@gmail.com', 'password': '1234'})
    token = request.json()['access_token']

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    path = '/users/profile/'
    request = client.get(BASE_URL + path, headers=headers)
    assert request.status_code == 200
    assert request.json()['profile']


@pytest.mark.skip
@pytest.mark.django_db()
def test_order_add_hash(login_resource_setup):
    Order.objects.create(add_hash='1234567890')
    path = "/auth/login/"
    request = client.post(BASE_URL + path, json={'email': 'root229@gmail.com', 'password': '1234'})
    token = request.json()['access_token']

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    path = "/users/profile/add_hash/"
    request = client.post(BASE_URL + path, json={'hash': '1234567890'}, headers=headers)
    assert request.status_code == 200
    assert request.json()['status'] == 'success added'

    path = '/users/profile/'
    request = client.get(BASE_URL + path, headers=headers)
    assert request.status_code == 200
    assert len(request.json()['profile']['orders']) > 0
