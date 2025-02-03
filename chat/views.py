from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .forms import SignUpForm
from .models import Profile, FriendRequest, Friendship, PrivateChat, Message, ChatGroup, GroupMessage
from django.contrib.auth.models import User
from django.db.models import Q
import uuid

class CustomLoginView(LoginView):
    template_name = "chat/LoginPage.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        # First get the response which will log the user in
        response = super().form_valid(form)
        
        # Now the user is logged in, set them as online
        self.request.user.profile.is_online = True
        self.request.user.profile.save()
        
        # Broadcast online status with a small delay to ensure WebSocket connections are established
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "online_status",
            {
                "type": "user_online",
                "user_id": self.request.user.id,
                "status": True
            }
        )
        
        # Send another broadcast after a brief delay to ensure all clients receive it
        from django.core.cache import cache
        cache.set(f'user_{self.request.user.id}_login_time', True, 2)  # Set a 2-second flag
        
        return response

    def get_success_url(self):
        url = super().get_success_url()
        # Add a parameter to trigger the WebSocket connection immediately
        return f"{url}?login=1"

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login-user')
    else:
        form = SignUpForm()
    return render(request, 'chat/signup.html', {'form': form})

@login_required
def home(request):
    # Get friend requests
    friend_requests = FriendRequest.objects.filter(
        to_user=request.user,
        status='pending'
    )
    # Get all friends
    friendships = Friendship.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    )
    friends = []
    for friendship in friendships:
        friend = friendship.user2 if friendship.user1 == request.user else friendship.user1
        friends.append({
            'user': friend,
            'nickname': friend.profile.nickname,
            'is_online': friend.profile.is_online,
            'friendship_id': friendship.id
        })
    
    context = {
        'friend_requests': friend_requests,
        'friends': friends
    }
    return render(request, 'chat/home.html', context)

@login_required
def search_users(request):
    query = request.GET.get('q', '')
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | 
            Q(profile__nickname__icontains=query)
        ).exclude(id=request.user.id)
        
        # Exclude existing friends and pending requests
        existing_friends = Friendship.objects.filter(
            Q(user1=request.user) | Q(user2=request.user)
        ).values_list('user1', 'user2')
        friend_ids = []
        for u1, u2 in existing_friends:
            friend_ids.extend([u1, u2])
        
        pending_requests = FriendRequest.objects.filter(
            Q(from_user=request.user) | Q(to_user=request.user),
            status='pending'
        ).values_list('from_user', 'to_user')
        for u1, u2 in pending_requests:
            friend_ids.extend([u1, u2])
            
        users = users.exclude(id__in=friend_ids)
    else:
        users = []
    
    return render(request, 'chat/search_users.html', {'users': users, 'query': query})

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    FriendRequest.objects.create(from_user=request.user, to_user=to_user)
    messages.success(request, f'Friend request sent to {to_user.profile.nickname}')
    return redirect('search_users')

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    friend_request.status = 'accepted'
    friend_request.save()
    
    # Create friendship
    friendship = Friendship.objects.create(
        user1=friend_request.from_user,
        user2=friend_request.to_user
    )
    # Create private chat room
    PrivateChat.objects.create(friendship=friendship)
    
    messages.success(request, f'You are now friends with {friend_request.from_user.profile.nickname}')
    return redirect('chat-page')

@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    friend_request.status = 'rejected'
    friend_request.save()
    messages.success(request, 'Friend request rejected')
    return redirect('chat-page')

@login_required
def chat_room(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id)
    if request.user not in [friendship.user1, friendship.user2]:
        messages.error(request, "You don't have permission to access this chat.")
        return redirect('chat-page')
    
    chat = friendship.privatechat
    friend = friendship.user2 if friendship.user1 == request.user else friendship.user1
    
    # Mark unread messages as read
    Message.objects.filter(
        chat=chat,
        sender=friend,
        is_read=False
    ).update(is_read=True)
    
    context = {
        'chat': chat,
        'friend': friend,
        'messages': chat.messages.all()
    }
    return render(request, 'chat/chat_room.html', context)

@login_required
def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('group_name')
        if name:
            group = ChatGroup.objects.create(
                name=name,
                host=request.user
            )
            group.members.add(request.user)
            messages.success(request, f'Group "{name}" created successfully! Share the ID: {group.group_id}')
            return redirect('group_chat', group_id=group.group_id)
        else:
            messages.error(request, 'Group name is required')
    return render(request, 'chat/create_group.html')

@login_required
def join_group(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        try:
            group_id = uuid.UUID(group_id)
            group = get_object_or_404(ChatGroup, group_id=group_id)
            if request.user not in group.members.all() and request.user != group.host:
                group.members.add(request.user)
                messages.success(request, f'Successfully joined group "{group.name}"')
            return redirect('group_chat', group_id=group.group_id)
        except (ValueError, TypeError):
            messages.error(request, 'Invalid group ID')
    return render(request, 'chat/join_group.html')

@login_required
def group_chat(request, group_id):
    group = get_object_or_404(ChatGroup, group_id=group_id)
    if request.user not in group.members.all() and request.user != group.host:
        messages.error(request, "You don't have permission to access this group.")
        return redirect('chat-page')
    
    context = {
        'group': group,
        'messages': group.messages.all(),
        'members': group.members.all(),
        'is_host': group.host == request.user
    }
    return render(request, 'chat/group_chat_room.html', context)

@login_required
def my_groups(request):
    hosted_groups = request.user.hosted_groups.all()
    member_groups = request.user.group_chats.all()
    
    context = {
        'hosted_groups': hosted_groups,
        'member_groups': member_groups
    }
    return render(request, 'chat/my_groups.html', context)
