import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(username='ADMINRAPRAP')
user.role = User.Role.ADMIN
user.save()

print("\n=== ADMINRAPRAP Account Updated ===")
print(f"Username: {user.username}")
print(f"Email: {user.email}")
print(f"is_staff: {user.is_staff}")
print(f"is_superuser: {user.is_superuser}")
print(f"is_active: {user.is_active}")
print(f"role: {user.role}")
print(f"\nADMINRAPRAP is now configured with ADMIN role!")
