from django.urls import re_path
from .consumers import *


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<friend>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/notification/(?P<user_id>\w+)/$', NotificationConsumer.as_asgi())
]

