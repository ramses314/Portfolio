import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Client


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        if hasattr(self, 'room_group_name'):
            _, request_id = self.room_group_name.split('_')
            clients = await database_sync_to_async(
                Client.objects.filter, thread_sensitive=True)(request_id__contains=request_id)
            await database_sync_to_async(clients.delete, thread_sensitive=True)()
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        method = text_data_json.get('method')
        request_id = text_data_json.get('request_id')
        channel = text_data_json.get('params').get('channel')

        if method == 'i' and channel == 'echo':
            echo = text_data_json.get('params').get('echo')
            await self.send(
                text_data=json.dumps(
                    {
                        "request_id": request_id,
                        "method": "i",
                        "params": {
                            "channel": "echo",
                            "echo": echo
                        },
                    }))

        if method == 's':
            self.room_name = str(request_id)
            self.room_group_name = f'{channel}_{request_id}'
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await database_sync_to_async(
                Client.objects.get_or_create,
                thread_sensitive=True)(request_id=self.room_group_name)
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "chat_message",
                    "message": {
                        "channel": channel,
                        "data": {
                            "type": "s",
                            "body": 'null',
                            "request_id": request_id,
                        },
                        "status": 200
                    },
                })

        if method == 'us':
            self.room_name = str(request_id)
            self.room_group_name = f'{channel}_{request_id}'
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "chat_message",
                    "message": {
                        "channel": channel,
                        "data": {
                            "type": "us",
                            "body": 'null',
                            "request_id": request_id,
                        },
                        "status": 200
                    },
                })
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
            a = await database_sync_to_async(
                Client.objects.filter, thread_sensitive=True)(request_id=self.room_group_name)
            await database_sync_to_async(a.delete, thread_sensitive=True)()

        if method == 'ping' and channel == 'ping':
            await self.send(
                text_data=json.dumps(
                    {
                        "message": {
                            "channel": "ping",
                            "data": {
                                "type": "ping",
                                "body": 'pong',
                                "request_id": request_id,
                            },
                            "status": 200
                        },
                    }))

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
