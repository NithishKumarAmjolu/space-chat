from django.urls import path
from chat import views
from django.contrib.auth import logout
from django.shortcuts import redirect
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def logout_view(request):
    # Set user as offline before logout
    if request.user.is_authenticated:
        user_id = request.user.id
        request.user.profile.is_online = False
        request.user.profile.save()
        
        # Broadcast offline status
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "online_status",
            {
                "type": "user_online",
                "user_id": user_id,
                "status": False
            }
        )
    logout(request)
    return redirect('login-user')

urlpatterns = [
    path('', views.home, name='chat-page'),
    path('signup/', views.signup, name='signup'),
    path('auth/login/', views.CustomLoginView.as_view(), name='login-user'),
    path('auth/logout/', logout_view, name='logout-user'),
    
    # Friend management
    path('search/', views.search_users, name='search_users'),
    path('send-request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept-request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject-request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    
    # Private Chat
    path('chat/<int:friendship_id>/', views.chat_room, name='chat_room'),
    
    # Group Chat
    path('groups/', views.my_groups, name='my_groups'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/join/', views.join_group, name='join_group'),
    path('groups/<uuid:group_id>/', views.group_chat, name='group_chat'),
]
