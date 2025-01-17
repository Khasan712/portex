from django.urls import re_path
from app.consumers import WebSocketConsumer

websocket_urlpatterns = [
    re_path(r'ws/connect/(?P<subdomain>[^/]+)/$', WebSocketConsumer.as_asgi()),
]
