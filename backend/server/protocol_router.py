from channels.routing import ProtocolTypeRouter

from server.django_asgi import django_asgi_app

asgi_app = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,

    # WebSocket chat handler
    # "websocket": channels_asgi_app
})
