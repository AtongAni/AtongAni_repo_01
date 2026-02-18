import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
users = User.objects.all().values('username', 'is_staff', 'is_superuser', 'is_active')

print("\n=== Current User Accounts ===")
for u in users:
    print(f"Username: {u['username']}")
    print(f"  is_staff: {u['is_staff']}, is_superuser: {u['is_superuser']}, is_active: {u['is_active']}")
    print()
