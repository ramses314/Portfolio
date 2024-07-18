"""
ASGI config for t3 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from applications.events import routing as events_routing


application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': URLRouter(events_routing.websocket_urlpatterns),
    })
