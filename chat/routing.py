from django.urls import re_path

from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<friend>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

