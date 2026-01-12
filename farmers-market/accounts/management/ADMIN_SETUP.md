# Admin User Setup Guide

## Creating the Admin User

### Option 1: Using Django Management Command (Recommended)

Run this command in the farmers-market directory:

```bash
python manage.py create_admin
```

This will create an admin user with default credentials:
- **Username**: Admin
- **Email**: admin@farmersmarket.com
- **Password**: admin123

### Option 2: Create with Custom Credentials

```bash
python manage.py create_admin --username YourAdminName --email admin@example.com --password yourpassword
```

### Option 3: Using Django Shell

```bash
python manage.py shell
```

Then in the Python shell:

```python
from accounts.models import User

admin = User.objects.create_superuser(
    username='Admin',
    email='admin@farmersmarket.com',
    password='admin123',
    role='ADMIN'
)
```

## Admin Credentials

After creation, use these to log in:
- **Username**: Admin
- **Email**: admin@farmersmarket.com
- **Password**: admin123 (or your custom password)

## Admin Features

### 1. **Admin Dashboard** (`/admin`)
   - View platform statistics
   - See recent users, posts, comments, and orders
   - Monitor platform activity in real-time

### 2. **API Endpoints** (Requires Admin Authentication)

- `GET /api/auth/admin/dashboard/` - Full dashboard data
- `GET /api/auth/admin/users/` - All users on the platform
- `GET /api/auth/admin/posts/` - All posts with details
- `GET /api/auth/admin/comments/` - All comments

### 3. **Django Admin Panel** (`/admin/` - Django default)
   - Create, edit, delete users
   - Manage all posts and comments
   - View and manage orders
   - Edit farmer profiles

## Admin Capabilities

The Admin user can:
- ✅ View all platform statistics
- ✅ Monitor all users (farmers, customers)
- ✅ See all posts and comments
- ✅ Track all orders
- ✅ View platform activity in real-time
- ✅ Access Django admin panel
- ✅ Manage content moderation (when implemented)

## Security Notes

⚠️ **Important**:
- Change the default password immediately in production
- Use strong, unique passwords for admin accounts
- The admin user has superuser privileges
- Store credentials securely
- Never commit passwords to version control

## Accessing Admin Dashboard in Frontend

1. Log in as Admin user
2. Navigate to the Admin Dashboard component
3. View statistics, recent activity, and all platform data

The dashboard automatically restricts access to users with `role=ADMIN`
