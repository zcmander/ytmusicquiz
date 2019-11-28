from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

from .consumers import GameConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                re_path(r'api/dashboard/(?P<game_id>\d+)/$', GameConsumer),
            ]
        )
    )
})
