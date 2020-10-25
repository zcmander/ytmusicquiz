from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from django.urls import re_path

from .consumers import GameConsumer, BackgroundConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                re_path(r'api/dashboard/$', GameConsumer),
            ]
        )
    ),
    'channel': ChannelNameRouter({
        'background-tasks': BackgroundConsumer
    })
})
