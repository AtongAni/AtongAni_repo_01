#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken

# Create or get test user
username = 'curl_test_farmer'
try:
    user = User.objects.get(username=username)
except User.DoesNotExist:
    user = User.objects.create_user(username=username, password='testpass')

refresh = RefreshToken.for_user(user)
print(str(refresh.access_token))
