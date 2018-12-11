from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, include
from django.conf.urls import url
import group.routing
import event.routing

# combine all websocket urls into single list
patterns = event.routing.websocket_urlpatterns + group.routing.websocket_urlpatterns

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                patterns
            )
        )
    )
})
