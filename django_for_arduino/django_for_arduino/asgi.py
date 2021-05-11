"""
ASGI config for django_for_arduino project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

# AMG: uncomment for HTTP ussage
# from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django_for_arduino.routing import websocket_urlPattern

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_for_arduino.settings')

# AMG: this is for HTTP, but I'm using websockets ;-)
#      if needed then uncomment
# application = get_asgi_application()

application = ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(
        URLRouter(
            websocket_urlPattern
        )
    ),
})
