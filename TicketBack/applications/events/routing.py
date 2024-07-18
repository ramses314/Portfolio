from django.urls import path

from applications.events import consumers as event_consumers

websocket_urlpatterns = [

    path(
        r'ws/connection/', event_consumers.ChatConsumer.as_asgi()
    ),

]
