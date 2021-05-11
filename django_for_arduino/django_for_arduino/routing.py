import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from django.urls import path
from frontend import consumer
websocket = str(os.environ["WEBSOCKET"])
websocket_urlPattern =[
    path(websocket, consumer.DashConsumer.as_asgi()),
]