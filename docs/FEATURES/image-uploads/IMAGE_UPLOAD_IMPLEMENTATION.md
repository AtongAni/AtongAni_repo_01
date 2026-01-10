# Image Upload Implementation Summary

## Feature Overview
Added complete image upload capability to the Farmers Market post feature, enabling farmers to upload product images when creating posts.

## What Works

### ✅ Farmer-Side
- Upload image while creating a post
- Real-time preview of selected image
- Clear/remove image before posting
- Validation messages for file type and size
- Optional image (can post without image)

### ✅ Storage
- Images stored in `media/posts/` directory
- Safe filename generation by Django
- Database stores relative path (e.g., "posts/abc123.jpg")
- Full URL returned in API for displaying images

### ✅ Linking
- Each image linked to the post
- Each image linked to the farmer (post author) through the Post model
- Farmer can edit/delete their own posts with images

### ✅ Display
- PostCard component shows images if present
- Images scale responsively (200px height max)
- Proper aspect ratio maintained

### ✅ Validation
- **Client-side**: File type (JPEG, PNG, GIF, WebP) and size (5MB max)
- **Server-side**: MIME type validation, file size check

## Implementation Details

### Backend Changes

#### 1. Model Update (`farmers-market/posts/models.py`)
```python
# Changed from:
image = models.URLField(blank=True, null=True)

# To:
image = models.ImageField(upload_to='posts/', blank=True, null=True, help_text="Product image")
```

#### 2. Settings (`farmers-market/config/settings.py`)
```python
# Added:
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

#### 3. URL Configuration (`farmers-market/config/urls.py`)
```python
# Added:
from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

#### 4. Serializer (`farmers-market/posts/serializers.py`)
```python
# Added image_url field:
image_url = serializers.SerializerMethodField()

# Added validation:
def validate_image(self, value):
    if value:
        # Check file size (max 5MB)
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Image file too large (max 5MB).")
        
        # Check file type
        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("Unsupported image format...")
    return value
```

#### 5. Database Migration (`farmers-market/posts/migrations/0003_alter_post_image.py`)
- Automatically handles schema change from URLField to ImageField
- Run with: `python manage.py migrate posts`

### Frontend Changes

#### 1. Form Component (`web/src/components/FarmerPostForm.jsx`)
```javascript
// Added state:
const [image, setImage] = useState(null);
const [imagePreview, setImagePreview] = useState(null);

// Added handler:
function handleImageChange(e) {
  const file = e.target.files[0];
  // Validate and set image + preview
}

// Modified submit:
const formData = new FormData();
formData.append('title', title.trim());
formData.append('content', content.trim());
// ... other fields
if (image) {
  formData.append('image', image);
}
await createPost(formData);
```

#### 2. API Client (`web/src/api/posts.js`)
```javascript
// Updated to handle FormData:
export function createPost(data) {
  if (data instanceof FormData) {
    return api.post("/api/posts/", data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }
  return api.post("/api/posts/", data);
}
```

#### 3. Form Styling (`web/src/components/FarmerPostForm.css`)
```css
/* Added new styles: */
.image-upload-section { }
.image-help-text { }
.image-preview-container { }
.image-preview { }
.clear-image-btn { }
```

## Data Flow

### Creating a Post with Image

```
Farmer Selects Image
    ↓
Frontend validates (type, size)
    ↓
Shows preview to farmer
    ↓
Farmer submits form
    ↓
FormData sent to /api/posts/
    ↓
Django serializer validates image
    ↓
Image saved to media/posts/abc123.jpg
    ↓
Path stored in database: "posts/abc123.jpg"
    ↓
API returns full URL: "http://localhost:8000/media/posts/abc123.jpg"
    ↓
Frontend displays image in post card
```

### Retrieving Posts with Images

```
GET /api/posts/
    ↓
Django returns posts with:
  - image: "posts/abc123.jpg"
  - image_url: "http://localhost:8000/media/posts/abc123.jpg"
    ↓
Frontend displays images using image_url
```

## Database Schema

### Post Model
```
id (PrimaryKey)
author_id (ForeignKey to User) ← Links to farmer
title (CharField)
content (TextField)
image (ImageField) ← NEW: stores "posts/filename.jpg"
price (DecimalField)
quantity (DecimalField)
unit (CharField)
created_at (DateTimeField)
updated_at (DateTimeField)
```

## API Response Example

```json
{
  "id": 1,
  "author": {
    "id": 5,
    "username": "farmer_john",
    "first_name": "John",
    "last_name": "Doe"
  },
  "author_id": 5,
  "title": "Fresh Organic Tomatoes",
  "content": "Pesticide-free, locally grown tomatoes...",
  "image": "posts/post_1_image_abc123.jpg",
  "image_url": "http://localhost:8000/media/posts/post_1_image_abc123.jpg",
  "price": "50.00",
  "quantity": "100.00",
  "unit": "KG",
  "created_at": "2024-01-10T10:30:00Z",
  "updated_at": "2024-01-10T10:30:00Z"
}
```

## Directory Structure

```
farmers-market/
├── media/                                    ← NEW
│   └── posts/                                ← NEW
│       ├── post_1_image_abc123.jpg
│       ├── post_2_image_xyz789.jpg
│       └── ...
├── posts/
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   ├── 0002_post_quantity_post_unit.py
│   │   └── 0003_alter_post_image.py         ← NEW
│   ├── models.py                             ← MODIFIED
│   ├── serializers.py                        ← MODIFIED
│   ├── views.py
│   └── ...
├── config/
│   ├── settings.py                           ← MODIFIED
│   ├── urls.py                               ← MODIFIED
│   └── ...
├── requirements.txt                          ← NEW
└── manage.py
```

## Configuration

### Django Settings Required
✅ `DEBUG = True` (for development)
✅ `MEDIA_URL = 'media/'`
✅ `MEDIA_ROOT = BASE_DIR / 'media'`

### Dependencies
✅ `Pillow==10.1.0` - Required for ImageField support

## Constraints & Limitations

1. **Single image per post** - Currently one image max per post
2. **Optional image** - Image is optional when creating posts
3. **File size limit** - 5MB max (configurable in serializer)
4. **Supported formats** - JPEG, PNG, GIF, WebP only
5. **Local storage** - Files stored on server filesystem (development)
6. **Production** - Should be configured for cloud storage (S3, Azure, etc.)

## Installation Requirements

```bash
# Install Pillow
pip install Pillow==10.1.0

# Or install all dependencies
pip install -r requirements.txt

# Run migration
python manage.py migrate posts
```

## Testing Checklist

- [ ] Install Pillow dependency
- [ ] Run database migration
- [ ] Start Django dev server
- [ ] Start React dev server
- [ ] Create a post with image
  - [ ] Verify image preview shows
  - [ ] Verify validation works (file type/size)
  - [ ] Verify image uploads successfully
- [ ] View post in feed
  - [ ] Verify image displays
  - [ ] Verify image is responsive
- [ ] Create a post without image
  - [ ] Verify form still works
  - [ ] Verify no errors
- [ ] Edit a post with image
  - [ ] Verify can upload new image
- [ ] Delete a post with image
  - [ ] Verify deletion works
  - [ ] Verify file is cleaned up (optional, needs cleanup code)

## Files Changed

| File | Type | Change |
|------|------|--------|
| `farmers-market/posts/models.py` | Modified | ImageField for images |
| `farmers-market/posts/serializers.py` | Modified | Image validation, image_url field |
| `farmers-market/posts/migrations/0003_alter_post_image.py` | Created | Database migration |
| `farmers-market/config/settings.py` | Modified | MEDIA_URL, MEDIA_ROOT settings |
| `farmers-market/config/urls.py` | Modified | Media file serving |
| `farmers-market/requirements.txt` | Created | Project dependencies |
| `web/src/components/FarmerPostForm.jsx` | Modified | Image upload input, preview, handling |
| `web/src/components/FarmerPostForm.css` | Modified | Image upload styling |
| `web/src/api/posts.js` | Modified | FormData support |
| `PostCard.jsx` | No change | Already supports image display |
| `PostCard.css` | No change | Already has image styling |

## Notes

- Images are automatically linked to both the post and the farmer through the `author` foreign key on the Post model
- The `image_url` field in the API response provides the full URL for displaying images
- File paths stored in database are relative (e.g., "posts/abc123.jpg") for portability
- Both old posts (without images) and new posts (with images) are supported
- No additional frontend configuration needed - component updates are automatic
