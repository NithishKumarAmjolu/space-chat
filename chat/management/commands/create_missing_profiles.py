from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from chat.models import Profile

class Command(BaseCommand):
    help = 'Creates missing profiles for users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        created_count = 0
        
        for user in users:
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={'nickname': user.username}
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created profile for user: {user.username}')
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {created_count} missing profiles'
        ))
