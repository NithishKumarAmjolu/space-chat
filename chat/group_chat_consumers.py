import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatGroup, GroupMessage, Profile
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connect attempt...")
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.room_group_name = f'group_{self.group_id}'
        self.user = self.scope['user']

        print(f"User {self.user.username} attempting to connect to group {self.group_id}")

        # Verify user is a member of the group
        is_member = await self.is_group_member()
        print(f"Is member check result: {is_member}")
        
        if not is_member:
            print("User is not a member, closing connection")
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print(f"Added to channel group: {self.room_group_name}")

        if self.scope["user"].is_authenticated:
            await self.accept()
            await self.update_user_status(True)
            print("WebSocket connection accepted")
        else:
            print("User not authenticated, closing connection")
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.update_user_status(False)

    async def receive(self, text_data):
        print(f"Received WebSocket message: {text_data}")
        data = json.loads(text_data)
        message_type = data.get('type', '')

        if message_type == 'message':
            message = data['message']
            print(f"Processing message: {message}")
            # Save message to database
            try:
                message_instance = await self.save_message(message)
                print(f"Message saved with ID: {message_instance.id}")
            except Exception as e:
                print(f"Error saving message: {str(e)}")
                return
            
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': self.user.username,
                    'nickname': await self.get_user_nickname(),
                    'message_id': str(message_instance.id)
                }
            )
        elif message_type == 'typing_start':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_indicator',
                    'username': self.user.username,
                    'nickname': await self.get_user_nickname(),
                    'is_typing': True
                }
            )
        elif message_type == 'typing_stop':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_indicator',
                    'username': self.user.username,
                    'nickname': await self.get_user_nickname(),
                    'is_typing': False
                }
            )

    async def chat_message(self, event):
        print(f"Broadcasting message to client: {event}")
        try:
            await self.send(text_data=json.dumps({
                'type': 'message',
                'message': event['message'],
                'username': event['username'],
                'nickname': event['nickname'],
                'message_id': event['message_id']
            }))
            print("Message broadcast successful")
        except Exception as e:
            print(f"Error broadcasting message: {str(e)}")

    async def typing_indicator(self, event):
        print(f"Broadcasting typing indicator: {event}")
        try:
            if event['username'] != self.user.username:
                await self.send(text_data=json.dumps({
                    'type': 'typing_indicator',
                    'username': event['username'],
                    'nickname': event['nickname'],
                    'is_typing': event['is_typing']
                }))
                print("Typing indicator broadcast successful")
        except Exception as e:
            print(f"Error broadcasting typing indicator: {str(e)}")

    @database_sync_to_async
    def save_message(self, message):
        group = ChatGroup.objects.get(group_id=self.group_id)
        return GroupMessage.objects.create(
            group=group,
            sender=self.user,
            content=message
        )

    @database_sync_to_async
    def is_group_member(self):
        try:
            group = ChatGroup.objects.get(group_id=self.group_id)
            return group.members.filter(id=self.user.id).exists() or group.host == self.user
        except ChatGroup.DoesNotExist:
            return False

    @database_sync_to_async
    def update_user_status(self, status):
        return Profile.objects.filter(user=self.user).update(is_online=status)

    @database_sync_to_async
    def get_user_nickname(self):
        return self.user.profile.nickname
