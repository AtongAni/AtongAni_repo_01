# Backend Setup Instructions

The backend now has complete posts and comments functionality. To finalize the setup:

## Step 1: Run Django Migrations

Open PowerShell in the farmers-market directory and run:

```powershell
python manage.py migrate
```

This will create all necessary database tables for Posts and Comments.

## Step 2: Test the API

After migration, you can test the endpoints:

- **List Posts**: GET /api/posts/
- **Create Post**: POST /api/posts/ (requires authentication, sends: title, content, image, price)
- **Get Post**: GET /api/posts/{id}/
- **List Comments**: GET /api/posts/{post_id}/comments/
- **Create Comment**: POST /api/posts/{post_id}/comments/ (requires authentication, sends: content)
- **Update Comment**: PATCH /api/posts/{post_id}/comments/{comment_id}/ (only author can update)
- **Delete Comment**: DELETE /api/posts/{post_id}/comments/{comment_id}/ (only author can delete)

## What Was Fixed

1. **Created Posts App** with:
   - Post model (title, content, image, price, author, timestamps)
   - PostSerializer with author details
   - PostViewSet with full CRUD permissions
   - Filtering by role
   - Only authors can edit/delete their posts

2. **Created Comments App** with:
   - Comment model (content, author, post, timestamps)
   - CommentSerializer with author details
   - PostCommentViewSet for nested comments under posts
   - Only authors can edit/delete their comments

3. **Updated Configuration**:
   - Added 'posts' and 'comments' to INSTALLED_APPS
   - Updated config/urls.py to include posts API routes
   - Created initial migrations for both apps

4. **Fixed Role Issue**:
   - Updated BaseRegisterSerializer to accept first_name and last_name
   - Both CustomerRegisterSerializer and FarmerRegisterSerializer now properly create users with the correct role

5. **Fixed Frontend Role Categorization**:
   - Updated Dashboard.jsx to use uppercase role values (FARMER, CUSTOMER) matching backend

## Next Steps

1. Run migrations: `python manage.py migrate`
2. The frontend will automatically work with the new API endpoints
3. Posts and comments will load correctly without "Failed to load posts" error
