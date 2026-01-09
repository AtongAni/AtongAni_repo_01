# Farmer Post Creation - Diagnostic Checklist

## Frontend Issues to Check (use browser DevTools)

### 1. **Token Storage**
```javascript
// Open browser console and run:
localStorage.getItem('accessToken')
// Should return a JWT token like: eyJ0eXAiOiJKV1QiLCJhbGc...
```
- ✅ If token exists, move to next check
- ❌ If null, user is NOT logged in → need to login first

### 2. **Token in Request Headers**
```javascript
// When you submit the form, watch Network tab:
// POST /api/posts/ should have:
// Authorization: Bearer eyJ0eXAi... (from Step 1)
```
- ✅ If header present, backend receives auth
- ❌ If header missing, token not being attached

### 3. **User Role Check**
```javascript
// Open browser console and run:
// First get user info by making a fetch call or checking Dashboard
// User.role should be "FARMER"
```
- ✅ If role is "FARMER", MyPosts tab should appear
- ❌ If role is "CUSTOMER", MyPosts tab won't appear

### 4. **API Response Status**
```javascript
// In Network tab, check POST /api/posts/ response:
// 201 Created = Success (response body has the new post)
// 400 Bad Request = Missing fields (check response body)
// 401 Unauthorized = Token not sent or invalid
// 403 Forbidden = Permission denied
// 500 Server Error = Backend crash
```

### 5. **Console Logs**
- Check for "Post creation error:" messages
- Check for "API Error:" interceptor logs
- Look for "Axios Request: Token attached" or "No token found"

## Backend Issues to Check

### 6. **PostViewSet Permissions**
File: `farmers-market/posts/views.py`
- `perform_create()` should have `self.request.user` as authenticated User
- Backend should receive JWT and validate it

### 7. **PostSerializer Fields**
File: `farmers-market/posts/serializers.py`
- `title`, `content` are required
- `price` is optional
- `image` is optional
- `author` should be auto-set from `self.request.user`

### 8. **Database**
- Check: `python manage.py shell`
```python
from posts.models import Post
Post.objects.all()  # Should see newly created posts
```

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "Failed to create post" | No token in request | Check Step 1-2, make sure logged in |
| "Failed to create post" | User not a FARMER | Check Step 3, register as FARMER |
| Empty FarmerPostForm missing | Role is CUSTOMER | Re-register with FARMER role |
| 400 Bad Request | Missing title/content | Fill in both fields |
| 401 Unauthorized | Token expired | Logout and login again |
| No error shown | Silent failure | Check console for errors |

## How to Test

1. **Open browser DevTools (F12)**
2. **Go to Network tab**
3. **Fill and submit FarmerPostForm**
4. **Look for POST /api/posts/ request**
5. **Check Status Code:**
   - 201 = Success ✅
   - 400+ = Error ❌
6. **Check Response body for error details**
7. **Check Console tab for error logs**

## What to Share with Debugging

When reporting the issue, include:
- Console error message
- Network tab Response body (the JSON error)
- Network tab Request Headers (especially Authorization header)
- User role from Dashboard display
