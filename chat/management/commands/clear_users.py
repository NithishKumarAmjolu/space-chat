from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from chat.models import Profile

class Command(BaseCommand):
    help = 'Clears all user data including profiles'

    def handle(self, *args, **kwargs):
        # Clear all profiles first (due to OneToOne relationship with User)
        Profile.objects.all().delete()
        self.stdout.write('Cleared all user profiles')
        
        # Clear all users
        User.objects.all().delete()
        self.stdout.write('Cleared all users')
        
        self.stdout.write(self.style.SUCCESS('Successfully cleared all user data'))
