# Debugging 500 Error on Post Creation

## What Changed

The backend now has better error handling and logging for post creation failures.

## How to Check Django Logs

### Option 1: Check Django Console Output
If Django is running in a terminal, look for error messages that appear when you try to create a post.

### Option 2: Run Django in Debug Mode

```bash
cd farmers-market
python manage.py runserver
```

The terminal will show stack traces for any 500 errors.

### Option 3: Check Django's Error Log File

```bash
# If you have a log file configured
tail -f logs/django.log
```

## Common 500 Error Causes

| Error | Cause | Fix |
|-------|-------|-----|
| `Request context is required` | Serializer not receiving request | ✅ Fixed in views.py `get_serializer_context()` |
| `You must be authenticated` | User not being passed correctly | ✅ Fixed in serializer validation |
| `author` field constraint error | Double-setting author | ✅ Fixed in perform_create |
| Field validation error | Title/content empty | Already validates in serializer |
| Database error | Schema mismatch | Run migrations: `python manage.py migrate` |

## What to Do

1. **Look at Django console output** when you try to post
2. **Share the full error stack trace** if you get one
3. **Check that migrations are applied:**
   ```bash
   cd farmers-market
   python manage.py migrate
   python manage.py migrate posts
   ```

4. **Verify the database schema:**
   ```bash
   python manage.py shell
   >>> from posts.models import Post
   >>> Post._meta.get_fields()
   ```

## Testing Manually

```bash
cd farmers-market
python manage.py shell
```

Then in the shell:
```python
from posts.models import Post
from accounts.models import User

# Get a user
user = User.objects.filter(role='FARMER').first()
if not user:
    print("No farmer user found!")
else:
    # Try creating a post
    post = Post.objects.create(
        author=user,
        title="Test Post",
        content="This is a test"
    )
    print(f"Created post: {post}")
```

## Frontend Error Message

The frontend will now show:
- ❌ `"Server error - please contact support or check backend logs"` for 500 errors
- This tells you to check the Django terminal/logs

## Next Steps

1. Try creating a post again
2. Check the Django console for any error messages
3. Share the exact error message from Django's console output
