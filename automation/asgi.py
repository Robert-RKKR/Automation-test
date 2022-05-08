"""
ASGI config for automation project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

# Python Import:
import os

# Django import:
from django.core.asgi import get_asgi_application

# Channels Import:
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Application Import:
from nap.routing import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'automation.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(URLRouter(ws_urlpatterns)),
})
