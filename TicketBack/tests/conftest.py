import uuid
import datetime

from django.utils import timezone
from selenium.webdriver.common.by import By

from applications.main.apps import MainConfig
from applications.sales import models
from applications.events.models import Ticket, Category, Event, Prize
from applications.main.models import Preference, TestBlock

from selenium import webdriver
import pytest

from applications.users.models import CustomUser


@pytest.fixture()
def event_resource_setup(request):

    for record in range(1, 5):
        Category.objects.create(
            title=f'Racing{record}'
        )
        Event.objects.create(
            title=f"Horse racing{record}",
            slug=f"horseracing{record}",
            content="etc...",
            expired= timezone.now() + datetime.timedelta(days=10),
            image="https://ie.wampi.ru/2022/12/12/SNIMOK-EKRANA-OT-2022-12-01-11-44-10.png",
            ticket_quantity=100,
            category=Category.objects.get(id=1),
            link="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
        Event.objects.create(
            title=f"Car racing{record}",
            slug=f"carracing{record}",
            content="etc...",
            expired= timezone.now() + datetime.timedelta(days=10),
            image="https://ie.wampi.ru/2022/12/12/SNIMOK-EKRANA-OT-2022-12-01-11-44-10.png",
            ticket_quantity=100,
            category=Category.objects.get(id=1),
            link="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
        Prize.objects.create(
            title="car",
            content="new",
            image="https://ie.wampi.ru/2022/12/12/SNIMOK-EKRANA-OT-2022-12-01-11-44-10.png",
            event=Event.objects.get(id=1)
        )
        Ticket.objects.create(
            event=Event.objects.get(id=1),
            number=record,
            price=100,
            qr_code="https://",
        )

    ticket = Ticket.objects.first()

    data_for_socket = {
        "action": "send",
        "request_id": "624ca49d-8943-4609-8430-76847c72176a",
        "method": "s",
        "params": {"channel": "ticket"}
    }

    context = {
        "data_for_socket": data_for_socket,
        'event': ticket.uuid
    }

    def resource_teardown():
        pass

    request.addfinalizer(resource_teardown)
    return context


@pytest.fixture()
def sales_resource_setup(request):
    '''
    orders with unoccupied tickets
    '''

    TestBlock.objects.create()

    models.Order.objects.create(
        user_uuid=uuid.uuid4(),
        name='order1',
        email='forwork31415@gmail.com',
        description='test_description',
        admin_comment='admin_comment',
    )

    Preference.objects.create(
        site_title='ticketcrush'
    )

    # PagaditoPreference.objects.create(
    #     wsk='b6aaef28722d599712233d748617ed25',
    #     uid='a91f0ae0d46a3c22e7026ad32d8e66af',
    #     url='https://sandbox-api.pagadito.com/v1/',
    # )

    Category.objects.create(
        title=f'sport'
    )

    Event.objects.create(
        title=f"sport",
        slug=f"sport",
        content="etc...",
        expired= timezone.now() + datetime.timedelta(days=10),
        image="https://ie.wampi.ru/2022/12/12/SNIMOK-EKRANA-OT-2022-12-01-11-44-10.png",
        ticket_quantity=100,
        category=Category.objects.first(),
        link="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )

    Ticket.objects.create(
        event=Event.objects.first(),
        number=101,
        price=100,
    )

    def resource_teardown():
        request.addfinalizer(resource_teardown)


@pytest.fixture()
def resource_setup_expanded(sales_resource_setup, request):
    """
    collected order and basic resource setup
    """

    category = Category.objects.create(
        title=f'casino'
    )

    order = models.Order.objects.create(
        user_uuid=uuid.uuid4(),
        name='order2',
        email='forwork31415@gmail.com',
        description='test_description',
        admin_comment='admin_comment',
    )

    event = Event.objects.create(
        title=f"xbet",
        slug=f"xbet",
        content="etc...",
        expired= timezone.now() + datetime.timedelta(days=10),
        image="https://ie.wampi.ru/2022/12/12/SNIMOK-EKRANA-OT-2022-12-01-11-44-10.png",
        ticket_quantity=100,
        category=category,
        link="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )

    Ticket.objects.create(
        event=event,
        number=101,
        price=100,
        order=order,
    )

    Ticket.objects.create(
        event=event,
        number=102,
        price=100,
    )

    template_for_send_order = {
        "front_uuid": f"{Preference.objects.first().front_uuid}",
        "user_uuid": "",
        "name": "Carlos",
        "email": "forwork31415@gmail.com",
        "phone": "0705102589",

        "card_number": "4111111111111111",
        "card_expired": "12/2030",
        "card_name": "Liki Liro",
        "card_cvv": "123",
    }

    context = {
        "template_for_send_order": template_for_send_order
    }

    def resource_teardown():
        request.addfinalizer(resource_teardown)

    return context


@pytest.fixture()
def cron_setup(request):
    scheduler = MainConfig.scheduler
    return scheduler


@pytest.fixture()
def selenium_connect(request):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1200x600')

    driver = webdriver.Chrome(options=options)
    driver.get("http://127.0.0.1:8000/test/")
    driver.find_element(by=By.NAME, value="username").send_keys("root")
    driver.find_element(by=By.NAME, value="password").send_keys("1234")
    driver.find_element(by=By.CLASS_NAME, value="btn-primary ").click()

    return driver


@pytest.fixture()
def websocket_setup(request, selenium_connect):

    # connect to socket event
    driver = selenium_connect

    # create new event
    driver.execute_script("window.open('');")
    windows = driver.window_handles
    driver.switch_to.window(windows[1])

    driver.get("http://127.0.0.1:8000/admin/events/event/add")
    driver.find_element(By.ID, 'id_title').send_keys("Villa in Portugalia")
    driver.find_element(By.ID, 'id_content').send_keys("content")
    driver.find_element(By.ID, 'id_link').send_keys("content")
    driver.find_element(By.ID, 'calendarlink0').click()
    driver.find_element(By.LINK_TEXT, '28').click()

    driver.find_element(By.XPATH,
                        '/html/body/div[1]/div[1]/div[2]/div/section/div/div/form/div/div[1]/div/div/div[8]/div/div/p/span[2]/a[1]').click()
    driver.find_element(By.ID, 'id_ticket_quantity').send_keys(10)

    driver.find_element(By.ID, 'select2-id_category-container').click()
    driver.find_elements(By.TAG_NAME, 'li')[-1].click()

    driver.find_element(By.ID, 'id_link').send_keys('https:example.com')
    driver.find_element(By.NAME, '_continue').click()

    # create new ticket
    driver.execute_script("window.open('');")
    windows = driver.window_handles
    driver.switch_to.window(windows[2])

    driver.get('http://127.0.0.1:8000/admin/events/ticket/add/')
    driver.find_element(By.XPATH, '/html/body/div/div[1]/div[2]/div/section/div/div/form/div/div[1]/div/div/div[2]/div/div/div[1]/span/span[1]/span').click()
    driver.find_elements(By.TAG_NAME, 'li')[-1].click()

    driver.find_element(By.ID, 'id_number').clear()
    driver.find_element(By.ID, 'id_number').send_keys(5)
    driver.find_element(By.ID, 'id_price').send_keys(5)
    driver.find_element(By.NAME, '_continue').click()

    def resource_teardown():
        # delete ticket
        driver.switch_to.window(windows[2])
        driver.find_element(By.LINK_TEXT, 'Delete').click()
        driver.find_element(By.CLASS_NAME, 'btn-danger').click()

        # delete event
        driver.switch_to.window(windows[1])
        driver.find_element(By.LINK_TEXT, 'Delete').click()
        driver.find_element(By.CLASS_NAME, 'btn-danger').click()

    request.addfinalizer(resource_teardown)

    return driver


@pytest.fixture()
def login_resource_setup(request):

    TestBlock.objects.create()

    CustomUser.objects.create_user(
        email='root229@gmail.com',
        password='1234'
    )
