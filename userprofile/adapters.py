from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import perform_login
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_user_search_fields(self):
        return ['email']

    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email')
        avatar_url = sociallogin.account.extra_data.get('picture')  # ✅ This is the Google profile image URL
        print("Details  : ",sociallogin.account.extra_data.get('picture'))
        if email:
            try:
                user = User.objects.get(email=email)
                user.avatar = avatar_url or user.avatar  # Only if you have a field for avatar
                user.save()

                # Link and login the existing user
                sociallogin.state['process'] = 'connect'
                perform_login(request, user, email_verification='optional')
                sociallogin.connect(request, user)
                raise ImmediateHttpResponse(redirect('profile'))
            except User.DoesNotExist:
                pass  # Continue normal flow

    # Optional override – make sure the signature matches!
    def new_user(self, request, sociallogin):
        return super().new_user(request, sociallogin)
