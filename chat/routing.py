from django.urls import re_path
from . import consumers, group_chat_consumers, online_status_consumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/group/(?P<group_id>[\w-]+)/$', group_chat_consumers.GroupChatConsumer.as_asgi()),
    re_path(r'ws/online_status/$', online_status_consumer.OnlineStatusConsumer.as_asgi()),
]
