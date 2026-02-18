# Image Upload Feature Implementation

## Overview
This document describes the image upload capability added to the Farmers Market post feature. Farmers can now upload product images when creating posts, and these images are stored on the server with paths saved in the database.

## Architecture

### Backend Components

#### 1. **Django Model** (`posts/models.py`)
- Changed `image` field from `URLField` to `ImageField`
- Stores images in the `posts/` subdirectory under the media folder
- Automatically creates relative file paths for database storage
- Linked to both the Post (parent) and the User/Author (farmer who posted it)

```python
image = models.ImageField(upload_to='posts/', blank=True, null=True, help_text="Product image")
```

#### 2. **Django Settings** (`config/settings.py`)
- Added media file configuration:
  - `MEDIA_URL = 'media/'` - URL path for accessing media files
  - `MEDIA_ROOT = BASE_DIR / 'media'` - Filesystem path where uploads are stored

#### 3. **URL Configuration** (`config/urls.py`)
- Added URL pattern to serve media files in development:
  ```python
  if settings.DEBUG:
      urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  ```

#### 4. **Serializer** (`posts/serializers.py`)
- Added `image_url` field to provide full URLs to uploaded images
- Added image validation:
  - Maximum file size: 5MB
  - Allowed formats: JPEG, PNG, GIF, WebP
- Updated to handle multipart/form-data requests

#### 5. **Database Migration** (`posts/migrations/0003_alter_post_image.py`)
- Migration to convert existing image fields from URLField to ImageField
- Handles backward compatibility with existing posts

### Frontend Components

#### 1. **FarmerPostForm Component** (`web/src/components/FarmerPostForm.jsx`)
Features:
- File input with image type restrictions (JPEG, PNG, GIF, WebP)
- Real-time image preview before submission
- File size validation (max 5MB on client-side)
- Clear/remove button for selected image
- Help text showing supported formats and size limit
- FormData submission for multipart uploads

#### 2. **API Handler** (`web/src/api/posts.js`)
- Detects FormData and sets appropriate headers
- Handles both JSON and multipart/form-data requests
- Updates both `createPost()` and `updatePost()` for file support

#### 3. **PostCard Component** (`web/src/components/PostCard.jsx`)
- Already displays images if `post.image_url` is available
- Shows image in a 200px height container with proper aspect ratio

#### 4. **Styling** (`web/src/components/FarmerPostForm.css`)
- New styles for image upload section:
  - `.image-upload-section` - Container for file input
  - `.image-preview-container` - Preview area with border
  - `.image-preview` - Image display (max 200px height)
  - `.clear-image-btn` - Remove button styling
- Responsive design for mobile devices

## File Structure

### Backend
```
farmers-market/
├── media/                          # New - uploaded files directory
│   └── posts/                      # Product images
│       └── post_id_image.jpg
├── posts/
│   ├── models.py                   # Updated with ImageField
│   ├── serializers.py              # Updated with image validation
│   ├── migrations/
│   │   └── 0003_alter_post_image.py    # New migration
├── config/
│   ├── settings.py                 # Updated with MEDIA settings
│   └── urls.py                     # Updated to serve media
└── requirements.txt                # New - includes Pillow
```

### Frontend
```
web/src/
├── components/
│   ├── FarmerPostForm.jsx          # Updated with image upload
│   ├── FarmerPostForm.css          # Updated with image styles
│   ├── PostCard.jsx                # Already supports image display
│   └── PostCard.css                # Already has image styling
└── api/
    └── posts.js                    # Updated for multipart requests
```

## Database Schema

### Post Model Fields
```
id (primary key)
author_id (foreign key to User)
title (CharField)
content (TextField)
image (ImageField) ← NEW - stores relative path like "posts/abc123.jpg"
image_url (virtual field in serializer) ← Returns full URL
price (DecimalField)
quantity (DecimalField)
unit (CharField)
created_at (DateTimeField)
updated_at (DateTimeField)
```

## Usage Flow

### Creating a Post with Image

1. **Farmer opens form**: FarmerPostForm component displays
2. **Selects image**: File input accepts image selection
3. **Preview shown**: Client-side preview rendered immediately
4. **Validation**: 
   - File type checked (JPEG, PNG, GIF, WebP)
   - File size validated (max 5MB)
   - Error messages shown if invalid
5. **Form submission**: FormData sent with:
   - title, content, price, quantity, unit (JSON fields)
   - image file (multipart/form-data)
6. **Backend processing**:
   - Serializer validates image field
   - File saved to `media/posts/` directory
   - Relative path stored in database
7. **Response**: Full image URL returned in API response
8. **Display**: PostCard shows image from returned `image_url`

### Retrieving Posts with Images

- `GET /api/posts/` returns array with `image_url` field
- Frontend displays images using returned URLs
- Images served from `http://localhost:8000/media/posts/...`

## Configuration Details

### Environment Variables
No additional environment variables required for basic setup.

### Production Deployment Considerations

When deploying to production:

1. **Media Storage**: Configure cloud storage (AWS S3, Azure Blob, etc.) instead of local filesystem
2. **Permissions**: Ensure web server has read access to media directory
3. **Security**: 
   - Implement file type validation on server
   - Consider resizing/compressing images
   - Set appropriate CORS headers for image URLs
4. **Static Files**: Separate media files from static files
5. **Performance**: Consider CDN for image distribution

## API Endpoints

### Create Post with Image
```
POST /api/posts/
Content-Type: multipart/form-data

Form Data:
- title: string
- content: string
- price: number (optional)
- quantity: number (optional)
- unit: string (optional, default: 'KG')
- image: file (optional, max 5MB)

Response:
{
  "id": 1,
  "author": {...},
  "title": "Fresh Tomatoes",
  "content": "Organic tomatoes...",
  "image": "posts/abc123.jpg",
  "image_url": "http://localhost:8000/media/posts/abc123.jpg",
  "price": 50.00,
  "quantity": 100,
  "unit": "KG",
  "created_at": "2024-01-10T10:00:00Z",
  "updated_at": "2024-01-10T10:00:00Z"
}
```

### Update Post with New Image
```
PATCH /api/posts/{id}/
Content-Type: multipart/form-data

Same form data structure as create
```

## Validation Rules

### Client-Side (Browser)
- File type: JPEG, PNG, GIF, WebP only
- File size: Maximum 5MB
- Real-time preview for user confirmation

### Server-Side (Django)
- File type validation: image/jpeg, image/png, image/gif, image/webp
- File size: Maximum 5MB
- Image field: Optional (blank=True, null=True)

## Limitations & Notes

1. **Images are optional**: Posts can be created without images
2. **Single image per post**: Currently supports one image per post
3. **No image editing**: Uploading a new image updates the post
4. **File naming**: Django auto-generates safe filenames
5. **No CDN**: Images served directly from server in development

## Installation & Setup

### Backend Setup

1. Install dependencies:
```bash
cd farmers-market
pip install -r requirements.txt
```

2. Apply migrations:
```bash
python manage.py migrate posts
```

3. Media directory will be created automatically on first upload

### Frontend Setup

No additional setup required. The React component handles file uploads automatically.

### Testing Image Upload

1. Start Django server: `python manage.py runserver`
2. Start React dev server: `npm run dev`
3. Log in as a farmer
4. Navigate to create post
5. Select and upload an image
6. Verify image appears in preview
7. Submit form
8. Verify image displays in post feed

## Troubleshooting

### Images not uploading
- Check if `media/` directory exists and has write permissions
- Verify Pillow is installed: `pip show Pillow`
- Check Django debug logs for validation errors

### Images not displaying
- Verify `MEDIA_URL` and `MEDIA_ROOT` in settings
- Check if URL patterns include media static files
- Inspect browser console for broken image URLs

### File size errors
- Increase limit in serializer validation if needed
- Check form input max file size restrictions

### CORS issues (in production)
- Add image domain to CORS_ALLOWED_ORIGINS
- Consider using CDN for image delivery

## Future Enhancements

1. **Image compression**: Auto-compress on upload
2. **Multiple images**: Support multiple images per post
3. **Thumbnails**: Generate thumbnail previews
4. **Image cropping**: Allow farmers to crop images
5. **Cloud storage**: AWS S3, Azure Blob integration
6. **Image optimization**: WebP conversion, responsive images
7. **Image gallery**: Slideshow for multiple images
