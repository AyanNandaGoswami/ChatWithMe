from django.urls import re_path
from .consumers import *


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<friend>\w+)/$', ChatConsumer.as_asgi()),
    re_path(
        r'ws/notification/(?P<user_uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$',
        NotificationConsumer.as_asgi()
    )
]

