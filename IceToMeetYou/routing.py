from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, include
from django.conf.urls import url
from group.consumers import GroupConsumer
from event.consumers import EventConsumer

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path("group/ws", GroupConsumer),
                path("event/ws", EventConsumer)
            ])
        )
    )
})
