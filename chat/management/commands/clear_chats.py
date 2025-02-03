from django.core.management.base import BaseCommand
from chat.models import Message, GroupMessage, ChatGroup, PrivateChat, Friendship, FriendRequest

class Command(BaseCommand):
    help = 'Clears all chat-related data including messages, groups, and friendships'

    def handle(self, *args, **kwargs):
        # Clear all messages
        Message.objects.all().delete()
        self.stdout.write('Cleared all private messages')
        
        # Clear all group messages
        GroupMessage.objects.all().delete()
        self.stdout.write('Cleared all group messages')
        
        # Clear all chat groups
        ChatGroup.objects.all().delete()
        self.stdout.write('Cleared all chat groups')
        
        # Clear all private chats
        PrivateChat.objects.all().delete()
        self.stdout.write('Cleared all private chats')
        
        # Clear all friendships
        Friendship.objects.all().delete()
        self.stdout.write('Cleared all friendships')
        
        # Clear all friend requests
        FriendRequest.objects.all().delete()
        self.stdout.write('Cleared all friend requests')
        
        self.stdout.write(self.style.SUCCESS('Successfully cleared all chat data'))
