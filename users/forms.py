from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class CustomSignupForm(forms.Form):
    username = forms.CharField(max_length=30, label='사용자 이름')

    def signup(self, request, user):
        user.username = self.cleaned_data['username']
        socialaccount = user.socialaccount_set.first()

        if socialaccount:
            user.social_type = socialaccount.provider  # 'google', 'kakao', ...
            user.social_id = socialaccount.uid
        user.save()
        return user


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")  # email을 원하지 않으면 "username"만