import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Set the settings module and initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'd09.settings')
django.setup()  # This ensures the app registry is loaded

# Import chat.routing after Django is set up
import chat.routing

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})