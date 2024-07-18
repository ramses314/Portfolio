import json
import pytest
from selenium.webdriver.common.by import By

from applications.events.consumers import ChatConsumer
from channels.testing import WebsocketCommunicator


@pytest.mark.asyncio
@pytest.mark.django_db()
async def test_connect_consumer(django_db_setup):
    communicator = WebsocketCommunicator(ChatConsumer(), "/ws/connection/")
    connected, _ = await communicator.connect()
    assert connected


@pytest.mark.parametrize('channel', ['event', 'ticket', 'order'])
@pytest.mark.asyncio
@pytest.mark.django_db()
async def test_websocket_connect_to_channel(channel):
    communicator = WebsocketCommunicator(ChatConsumer(), "/ws/connection/")
    connected, _ = await communicator.connect()
    assert connected
    message = {
        "action": "send",
        "request_id": "89798987879",
        "method": 's',
        "params": {"channel": f"{channel}"}
    }
    await communicator.send_json_to(message)
    response = await communicator.receive_json_from()
    assert response == {
        "message": {
            "channel": f"{channel}",
            "data": {
                "type": "s",
                "body": 'null',
                "request_id": "89798987879",
            },
            "status": 200
        }
    }
    await communicator.disconnect()


@pytest.mark.parametrize('channel', ['event', 'ticket', 'order'])
@pytest.mark.asyncio
@pytest.mark.django_db()
async def test_websocket_connect_and_unconnect_from_channel(channel):
    communicator = WebsocketCommunicator(ChatConsumer(), "/ws/connection/")
    connected, _ = await communicator.connect()
    assert connected
    # connect
    message = {"action": "send", "request_id": "89798987879", "method": 's', "params": {"channel": f"{channel}"}}
    await communicator.send_json_to(message)
    response = await communicator.receive_json_from()
    assert response == {"message": {
        "channel": f"{channel}",
        "data": {"type": "s", "body": 'null', "request_id": "89798987879"}, "status": 200}
    }
    # unconnect
    message = {"action": "send", "request_id": "89798987879", "method": 'us', "params": {"channel": f"{channel}"}}
    await communicator.send_json_to(message)
    response = await communicator.receive_json_from()
    assert response == {"message": {
        "channel": f"{channel}",
        "data": {"type": "us", "body": 'null', "request_id": "89798987879"}, "status": 200}
    }
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db()
async def test_websocket_echo():
    communicator = WebsocketCommunicator(ChatConsumer(), "/ws/connection/")
    connected, _ = await communicator.connect()
    assert connected
    message = {
        "request_id": "98787987",
        "method": 'i',
        "params": {"channel":"echo", "echo": {'111': '22222'}}
    }
    await communicator.send_json_to(message)
    response = await communicator.receive_json_from()
    assert response == {
            "request_id": "98787987",
            "method": "i",
            "params": {
                "channel": "echo",
                "echo": {
                    "111": "22222"
                }
            }
        }
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db()
async def test_websocket_ping():
    communicator = WebsocketCommunicator(ChatConsumer(), "/ws/connection/")
    connected, _ = await communicator.connect()
    assert connected
    message = {
        "request_id": "6756775687",
        "method": "ping",
        "params": {"channel":"ping"}
    }
    await communicator.send_json_to(message)
    response = await communicator.receive_json_from()
    assert response == {
        "message": {
            "channel": "ping",
            "data": {"type": "ping", "body": "pong", "request_id": "6756775687"},
            "status": 200
        }
    }
    await communicator.disconnect()


@pytest.mark.ws_selenium
@pytest.mark.asyncio
async def test_websocket_event_group(selenium_connect):

    # connect to socket event
    driver = selenium_connect
    driver.find_element(by=By.ID, value="get_method_one_event").click()

    # create new event
    driver.execute_script("window.open('');")
    windows = driver.window_handles
    driver.switch_to.window(windows[1])
    # fill fields
    driver.get("http://127.0.0.1:8000/admin/events/event/add")
    driver.find_element(By.ID, 'id_title').send_keys("Villa in Portugalia")
    driver.find_element(By.ID, 'id_content').send_keys("content")
    driver.find_element(By.ID, 'id_link').send_keys("content")
    driver.find_element(By.ID, 'calendarlink0').click()
    driver.find_element(By.LINK_TEXT, '28').click()

    driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/section/div/div/form/div/div[1]/div/div/div[8]/div/div/p/span[2]/a[1]').click()
    driver.find_element(By.ID, 'id_ticket_quantity').send_keys(10)

    driver.find_element(By.ID, 'select2-id_category-container').click()
    driver.find_elements(By.TAG_NAME, 'li')[-1].click()
    driver.find_element(By.ID, 'id_link').send_keys('https:example.com')
    # save
    driver.find_element(By.CLASS_NAME, 'btn-success').click()

    # delete event
    driver.find_element(By.ID, 'searchbar').send_keys('Villa in Portugalia')
    driver.find_element(By.CLASS_NAME, 'btn-primary').click()
    driver.find_element(By.LINK_TEXT, 'Villa in Portugalia').click()
    driver.find_element(By.LINK_TEXT, 'Delete').click()
    driver.find_element(By.CLASS_NAME, 'btn-danger').click()

    # get response from socket
    driver.switch_to.window(windows[0])
    response = driver.find_element(by=By.ID, value='response').text
    response = json.loads(response)

    assert response['message']['channel'] == 'event'
    assert response['message']['data']['body']['event']['title'] == 'Villa in Portugalia'
    assert response['message']['status'] == 200


@pytest.mark.ws_selenium
@pytest.mark.asyncio
async def test_websocket_ticket_group(selenium_connect):

    driver = selenium_connect
    driver.find_element(by=By.ID, value="get_method_one_ticket").click()

    # change some ticket
    driver.execute_script("window.open('');")
    windows = driver.window_handles
    driver.switch_to.window(windows[1])
    driver.get('http://127.0.0.1:8000/admin/events/ticket/')
    driver.find_element(By.XPATH, '/html/body/div/div[1]/div[2]/div/section/div/div[2]/div/form/div/div/div[1]/div/div[2]/div/table/tbody/tr[1]/th/a').click()
    old_price = driver.find_element(By.ID, 'id_price').get_attribute('value')
    driver.find_element(By.ID, 'id_price').clear()
    driver.find_element(By.ID, 'id_price').send_keys(35.75)
    driver.find_element(By.NAME, '_continue').click()

    driver.switch_to.window(windows[0])
    response = driver.find_element(by=By.ID, value='response').text
    response = json.loads(response)

    assert response['message']['channel'] == 'ticket'
    assert response['message']['data']['body']['ticket']['price'] == '35.75'
    assert response['message']['status'] == 200

    # return old price
    driver.switch_to.window(windows[1])
    driver.find_element(By.ID, 'id_price').clear()
    driver.find_element(By.ID, 'id_price').send_keys(old_price)
    driver.find_element(By.NAME, '_continue').click()


@pytest.mark.ws_selenium
@pytest.mark.asyncio
async def test_websocket_all_tickets_are_sold(websocket_setup):

    driver = websocket_setup
    windows = driver.window_handles
    driver.switch_to.window(windows[0])
    driver.find_element(by=By.ID, value="get_method_one_event").click()
    driver.switch_to.window(windows[2])
    # change status in ticket
    driver.find_element(By.XPATH,
            '/html/body/div/div[1]/div[2]/div/section/div/div/form/div/div[1]/div/div/div[1]/div/div/span/span[1]/span').click()
    driver.find_element(By.XPATH, '/html/body/span/span/span[2]/ul/li[1]').click()
    driver.find_element(By.NAME, '_continue').click()
    # get response from socket
    driver.switch_to.window(windows[0])
    response = driver.find_element(by=By.ID, value='response').text
    response = json.loads(response)

    assert response['message']['channel'] == 'event'
    assert response['message']['data']['body']['message'] == 'All tickets are sold in event'
    assert response['message']['status'] == 200


@pytest.mark.ws_selenium
@pytest.mark.asyncio
async def test_websocket_send_number_of_open_tickets(websocket_setup):
    # create second tickets
    driver = websocket_setup
    driver.execute_script("window.open('');")
    windows = driver.window_handles
    driver.switch_to.window(windows[3])
    driver.get('http://127.0.0.1:8000/admin/events/ticket/add/')
    driver.find_element(By.XPATH,
                        '/html/body/div/div[1]/div[2]/div/section/div/div/form/div/div[1]/div/div/div[2]/div/div/div[1]/span/span[1]/span').click()
    driver.find_elements(By.TAG_NAME, 'li')[-1].click()
    driver.find_element(By.ID, 'id_number').clear()
    driver.find_element(By.ID, 'id_number').send_keys(6)
    driver.find_element(By.ID, 'id_price').send_keys(6)
    driver.find_element(By.NAME, '_continue').click()

    driver.switch_to.window(windows[0])
    driver.find_element(by=By.ID, value="get_method_one_event").click()

    # first ticket will be sold
    driver.switch_to.window(windows[2])
    driver.find_element(By.XPATH,
                        '/html/body/div/div[1]/div[2]/div/section/div/div/form/div/div[1]/div/div/div[1]/div/div/span/span[1]/span').click()
    driver.find_element(By.XPATH, '/html/body/span/span/span[2]/ul/li[1]').click()
    driver.find_element(By.NAME, '_continue').click()

    # return to test.html
    driver.switch_to.window(windows[0])
    response = driver.find_element(by=By.ID, value='response').text
    response = json.loads(response)

    #delete tickets 2
    driver.switch_to.window(windows[3])
    driver.find_element(By.LINK_TEXT, 'Delete').click()
    driver.find_element(By.CLASS_NAME, 'btn-danger').click()

    assert response['message']['channel'] == 'event'
    assert response['message']['data']['body']['message'] == 'ticket is sold'
    assert response['message']['data']['body']['counter']
    assert response['message']['status'] == 200
