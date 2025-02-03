from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignUpForm(UserCreationForm):
    nickname = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'nickname', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        nickname = self.cleaned_data['nickname']
        if commit:
            user.save()
            # Create or update profile
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={'nickname': nickname}
            )
            if not created:
                profile.nickname = nickname
                profile.save()
        return user
