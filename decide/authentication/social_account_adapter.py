from django.contrib.auth import get_user_model
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from rest_framework.response import Response
from django.shortcuts import redirect, render

User = get_user_model()

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):

        if sociallogin.is_existing:
            return

        if 'email' not in sociallogin.account.extra_data:
            return
        try:
            user = User.objects.get(email=sociallogin.user.email)
            sociallogin.connect(request, user)
            return redirect('accounts/social/login')
        except User.DoesNotExist:
            pass