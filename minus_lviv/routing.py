from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from messanger import consumers

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    re_path(r"^(?P<pk>[0-9]+)/$", consumers.LiveuserConsumer),
                    re_path(r'^messanger/(?P<pk>[0-9]+)/$', consumers.MessangerConsumer),
                ]
            )
        )
    }
)