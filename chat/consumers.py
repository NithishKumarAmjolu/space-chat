import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, PrivateChat, Profile
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connect attempt...")
        try:
            self.chat_id = self.scope['url_route']['kwargs']['chat_id']
            self.room_group_name = f'chat_{self.chat_id}'
            self.user = self.scope['user']

            print(f"User {self.user.username} attempting to connect to chat {self.chat_id}")

            # Verify chat exists and user has access
            chat_exists = await self.verify_chat_access()
            if not chat_exists:
                print(f"Chat {self.chat_id} not found or user has no access")
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
        except Exception as e:
            print(f"Error in connect: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.update_user_status(False)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type', '')

        if message_type == 'message':
            message = data['message']
            # Save message to database
            message_instance = await self.save_message(message)
            
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': self.user.username,
                    'message_id': str(message_instance.id)
                }
            )
        elif message_type in ['typing_start', 'typing_stop']:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': message_type,
                    'username': self.user.username
                }
            )
        elif message_type == 'mark_read':
            await self.mark_messages_as_read()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message_read',
                    'username': self.user.username
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'username': event['username'],
            'message_id': event['message_id']
        }))

    async def typing_start(self, event):
        if event['username'] != self.user.username:
            await self.send(text_data=json.dumps({
                'type': 'typing_start',
                'username': event['username']
            }))

    async def typing_stop(self, event):
        if event['username'] != self.user.username:
            await self.send(text_data=json.dumps({
                'type': 'typing_stop',
                'username': event['username']
            }))

    async def message_read(self, event):
        if event['username'] != self.user.username:
            await self.send(text_data=json.dumps({
                'type': 'message_read',
                'username': event['username']
            }))

    @database_sync_to_async
    def verify_chat_access(self):
        try:
            chat = PrivateChat.objects.get(id=self.chat_id)
            # Check if user is either user1 or user2 in the friendship
            return (chat.friendship.user1_id == self.user.id or 
                   chat.friendship.user2_id == self.user.id)
        except PrivateChat.DoesNotExist:
            print(f"Chat {self.chat_id} does not exist")
            return False
        except Exception as e:
            print(f"Error verifying chat access: {str(e)}")
            return False

    @database_sync_to_async
    def save_message(self, message):
        try:
            chat = PrivateChat.objects.get(id=self.chat_id)
            return Message.objects.create(
                chat=chat,
                sender=self.user,
                content=message
            )
        except Exception as e:
            print(f"Error saving message: {str(e)}")
            raise

    @database_sync_to_async
    def mark_messages_as_read(self):
        chat = PrivateChat.objects.get(id=self.chat_id)
        Message.objects.filter(
            chat=chat,
            sender__id=self.user.id,
            is_read=False
        ).update(is_read=True)

    @database_sync_to_async
    def update_user_status(self, status):
        return Profile.objects.filter(user=self.user).update(is_online=status)
