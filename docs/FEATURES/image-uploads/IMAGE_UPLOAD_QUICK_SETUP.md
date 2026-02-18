# Image Upload Feature - Quick Setup Guide

## What Was Added

Farmers can now upload product images when creating posts. Images are:
- ✅ Stored in a dedicated `media/posts/` folder
- ✅ Database stores the file path linked to the post
- ✅ Associated with both the post and the farmer who created it
- ✅ Validated for file type and size
- ✅ Displayed in the post feed with proper styling

## Installation Steps

### Step 1: Install Pillow (Backend Image Support)

```bash
cd farmers-market
pip install Pillow==10.1.0
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

### Step 2: Apply Database Migration

```bash
python manage.py migrate posts
```

This creates the updated Post model schema with the ImageField.

### Step 3: Start the Development Server

```bash
python manage.py runserver
```

The server will automatically serve media files from `http://localhost:8000/media/`

## Frontend - No Installation Needed

The React components are already updated and ready to use:
- ✅ FarmerPostForm - File upload input with preview
- ✅ PostCard - Image display for posts with images
- ✅ API client - Handles multipart/form-data submissions

## Testing the Feature

1. Navigate to Dashboard/Create Post page
2. Look for new "Product Image" section in the form
3. Select an image (JPEG, PNG, GIF, or WebP)
4. See a preview before posting
5. Submit the post
6. View the post in the feed - image will display if uploaded

## Key Features

### Form Features
- 📸 File input with image type restrictions
- 👁️ Real-time image preview
- ❌ Clear/remove button for selected image
- 📝 Help text showing supported formats and size limit (5MB max)
- ✔️ Client-side validation before submission

### Backend Features
- 🛡️ Server-side file type and size validation
- 📁 Automatic image storage in `media/posts/` directory
- 🔗 Database stores file path with post
- 👤 Images linked to both post and author/farmer
- 🔒 Safe filename generation

### Display Features
- 🖼️ Images display in post cards
- 📐 Responsive image sizing (200px height)
- 🎨 Proper aspect ratio preservation

## File Organization

```
farmers-market/
├── media/                    ← NEW: User uploads folder
│   └── posts/               ← Product images stored here
│       └── filename.jpg
├── posts/
│   ├── migrations/
│   │   └── 0003_alter_post_image.py    ← NEW: Migration
│   ├── models.py            ← Updated (ImageField)
│   └── serializers.py       ← Updated (validation)
├── config/
│   ├── settings.py          ← Updated (MEDIA_* settings)
│   └── urls.py              ← Updated (media URLs)
└── requirements.txt         ← NEW: Dependencies
```

## API Usage

### Create Post with Image
```javascript
const formData = new FormData();
formData.append('title', 'Fresh Tomatoes');
formData.append('content', 'Organic, pesticide-free...');
formData.append('price', 50.00);
formData.append('quantity', 100);
formData.append('unit', 'KG');
formData.append('image', imageFile);

await fetch('/api/posts/', {
  method: 'POST',
  body: formData  // Not JSON!
  // Don't set Content-Type header - browser will set it
});
```

## Validation Rules

### Client-Side
- ✅ File types: JPEG, PNG, GIF, WebP
- ✅ Max size: 5MB

### Server-Side
- ✅ File type validation (MIME type check)
- ✅ File size validation (5MB limit)
- ✅ Optional field (can create post without image)

## Database Changes

The Post model now has:
- `image`: FileField storing the path (e.g., "posts/abc123.jpg")
- `image_url`: Virtual field in API response with full URL

```
GET /api/posts/ returns:
{
  ...
  "image": "posts/abc123.jpg",
  "image_url": "http://localhost:8000/media/posts/abc123.jpg",
  ...
}
```

## Troubleshooting

### "Pillow is not installed"
```bash
pip install Pillow
```

### "media folder not found"
- Run: `python manage.py migrate`
- Create the folder: `mkdir media`
- The `media/posts/` subfolder will be created automatically on first upload

### Images not showing in posts
- Check if `MEDIA_URL` is set in settings (it is: `'media/'`)
- Verify Django dev server is running
- Check browser console for 404 errors on image URLs

### File upload fails
- Check file size (must be < 5MB)
- Check file format (JPEG, PNG, GIF, or WebP only)
- Check Django server logs for detailed error messages

## Production Deployment

For production, configure cloud storage (AWS S3, Azure Blob, etc.) instead of local filesystem:

1. Update `DEFAULT_FILE_STORAGE` in settings.py
2. Configure storage backend credentials
3. Update `MEDIA_URL` to point to cloud CDN
4. Remove the local media URL pattern from urls.py

See `IMAGE_UPLOAD_DOCUMENTATION.md` for detailed production setup.

## Files Modified/Created

### Created
- ✅ `farmers-market/requirements.txt` - Python dependencies
- ✅ `farmers-market/posts/migrations/0003_alter_post_image.py` - DB migration
- ✅ `IMAGE_UPLOAD_DOCUMENTATION.md` - Full documentation

### Modified
- ✅ `farmers-market/posts/models.py` - ImageField added
- ✅ `farmers-market/posts/serializers.py` - Image validation added
- ✅ `farmers-market/config/settings.py` - MEDIA settings added
- ✅ `farmers-market/config/urls.py` - Media serving enabled
- ✅ `web/src/components/FarmerPostForm.jsx` - File upload input added
- ✅ `web/src/components/FarmerPostForm.css` - Image upload styling added
- ✅ `web/src/api/posts.js` - Multipart form support added

## Next Steps

1. Install Pillow: `pip install Pillow`
2. Run migration: `python manage.py migrate`
3. Start server: `python manage.py runserver`
4. Test in browser at `http://localhost:3000`

Enjoy! 🎉
