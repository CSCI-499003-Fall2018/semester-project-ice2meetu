from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, include
import group.routing
# import event.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            group.routing.websocket_urlpatterns 
            # + event.routing.websocket_urlpatterns
        )
    ),
})
