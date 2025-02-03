import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Profile, User
from django.db.models import Q

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("online_status", self.channel_name)
        await self.accept()
        
        # Send current online users to the newly connected client
        online_users = await self.get_online_users()
        for user_id in online_users:
            await self.send(text_data=json.dumps({
                'type': 'user_status',
                'user_id': user_id,
                'status': True
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("online_status", self.channel_name)

    async def user_online(self, event):
        """
        Send user online status to WebSocket.
        """
        await self.send(text_data=json.dumps({
            'type': 'user_status',
            'user_id': event['user_id'],
            'status': event['status']
        }))

    @database_sync_to_async
    def update_user_status(self, user_id, status):
        Profile.objects.filter(user_id=user_id).update(is_online=status)

    @database_sync_to_async
    def get_online_users(self):
        # Get all online users
        return list(Profile.objects.filter(is_online=True).values_list('user_id', flat=True))
