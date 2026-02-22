#!/usr/bin/env python
"""Quick test script to verify farmer harvest profile creation"""
import os
import sys
import django
from decimal import Decimal
from datetime import date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User  # Use custom User model
from django.test import Client
from rest_framework_simplejwt.tokens import RefreshToken
import json

# Get or create a test farmer user
test_username = "testfarmer123"
try:
    farmer = User.objects.get(username=test_username)
    print(f"[INFO] Using existing test farmer: {farmer.username}")
except User.DoesNotExist:
    farmer = User.objects.create_user(username=test_username, password="testpass123", email="farmer@test.com")
    print(f"[INFO] Created new test farmer: {farmer.username}")

# Get JWT token for the user
refresh = RefreshToken.for_user(farmer)
access_token = str(refresh.access_token)
print(f"[INFO] Got access token for {farmer.username}")

# Prepare the test data
test_payload = {
    "land_size": 2.5,
    "land_size_unit": "hectares",
    "crop_type": "Rice and Wheat",
    "previous_harvest_quantity": 500.0,
    "previous_harvest_unit": "KG",
    "previous_harvest_date": "2025-06-15",
    "farming_experience_years": 10,
    "location": "Maharashtra, India",
    "notes": "Testing farmer profile creation",
}

print(f"\n[INFO] Test payload: {json.dumps(test_payload, indent=2)}")

# Make the API request using Django client
client = Client()
print(f"\n[INFO] Making POST request to /api/farmer-harvest-profile/")

response = client.post(
    '/api/farmer-harvest-profile/',
    data=json.dumps(test_payload),
    content_type='application/json',
    HTTP_AUTHORIZATION=f'Bearer {access_token}'
)

print(f"\n[RESPONSE] Status Code: {response.status_code}")
print(f"[RESPONSE] Content-Type: {response.get('content-type')}")
print(f"[RESPONSE] Body: {response.content.decode()}")

if response.status_code != 201:
    print(f"\n[ERROR] Unexpected status code!")
    try:
        response_data = json.loads(response.content)
        print(f"[ERROR] Response data: {json.dumps(response_data, indent=2)}")
    except:
        print(f"[ERROR] Could not parse response as JSON")
else:
    print(f"\n[SUCCESS] Profile created successfully!")
    try:
        response_data = json.loads(response.content)
        print(f"[SUCCESS] Response: {json.dumps(response_data, indent=2)}")
    except:
        pass
