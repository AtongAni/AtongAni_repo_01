# Multi-Image Posts - Technical Reference

**Status:** ✅ Complete | **Version:** 1.0.0

---

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Database Schema](#database-schema)
3. [API Endpoints](#api-endpoints)
4. [Frontend Components](#frontend-components)
5. [Image Validation](#image-validation)
6. [Error Handling](#error-handling)
7. [Known Limitations](#known-limitations)

---

## Architecture Overview

### System Flow

```
User Creates Post
    ↓
FarmerPostForm validates inputs + images
    ↓
POST /api/posts/ (Create post)
    ↓
Get post ID from response
    ↓
POST /api/posts/{id}/upload_images/ (Upload all images)
    ↓
Success → Display in gallery
    ↓
Feed renders PostCard with images
    ↓
User clicks gallery → Opens full-screen modal
```

### Component Interaction

```
FarmerPostForm
├── Validates title, description, price, quantity
├── Handles file input (1-15 images)
├── Shows preview grid
├── Creates post via createPost() API
├── Uploads images via uploadPostImages() API
└── Manages form state + errors

PostCard
├── Receives post with images array
├── Displays first image as main
├── Shows thumbnail strip of all images
├── Allows clicking thumbnails to switch
├── Modal for full-screen viewing
├── Keyboard navigation (arrow keys)
└── Click outside to close modal
```

---

## Database Schema

### PostImage Model

```python
class PostImage(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='post_images/',
        validators=[
            validate_image_file_size,
            validate_image_format
        ]
    )
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
```

### Migration

**File:** `posts/migrations/0004_postimage.py`

**Status:** ✅ Executed

**Tables Created:**
- `posts_postimage` (id, post_id, image, order, created_at)

### Relationships

```
Post (1)
  └── (1:N) → PostImage (N)
        └── (deleted when Post deleted via CASCADE)
```

---

## API Endpoints

### Upload Images

**POST** `/api/posts/{post_id}/upload_images/`

**Purpose:** Upload up to 15 image files to an existing post

**Request:**
```
Content-Type: multipart/form-data

Body:
  images: [File, File, ...] (up to 15 files)
```

**Success Response:** (201)
```json
{
  "images": [
    {
      "id": 1,
      "image": "http://127.0.0.1:8000/media/post_images/abc123.jpg",
      "order": 0,
      "created_at": "2026-01-10T10:30:00Z"
    },
    {
      "id": 2,
      "image": "http://127.0.0.1:8000/media/post_images/def456.jpg",
      "order": 1,
      "created_at": "2026-01-10T10:30:01Z"
    }
  ]
}
```

**Error Responses:**

| Status | Error | Cause |
|--------|-------|-------|
| 400 | `"No images provided"` | Request body empty |
| 400 | `"Too many images"` | More than 15 files |
| 400 | `"Image file too large"` | File > 5MB |
| 400 | `"Invalid file format"` | Non-image file |
| 404 | `"Post not found"` | Invalid post_id |
| 403 | `"You don't have permission"` | Not post owner |

**Client Code:**
```javascript
// frontend/api/posts.js
export const uploadPostImages = async (postId, files) => {
  const formData = new FormData();
  files.forEach((file) => formData.append('images', file));
  
  const response = await api.post(
    `/api/posts/${postId}/upload_images/`,
    formData
  );
  return response.data;
};
```

---

### Delete Image

**DELETE** `/api/posts/{post_id}/delete_image/{image_id}/`

**Purpose:** Remove a single image from a post

**Success Response:** (204 No Content)

**Error Responses:**

| Status | Error | Cause |
|--------|-------|-------|
| 404 | Image not found | Invalid image_id |
| 403 | Permission denied | Not post owner |

**Client Code:**
```javascript
// frontend/api/posts.js
export const deletePostImage = async (postId, imageId) => {
  await api.delete(
    `/api/posts/${postId}/delete_image/${imageId}/`
  );
};
```

---

## Frontend Components

### FarmerPostForm.jsx

**Purpose:** Collects post data and images, validates, submits

**Key State:**
```javascript
const [formData, setFormData] = useState({
  title: '',
  description: '',
  price: '',
  quantity: '',
  unit: ''
});
const [selectedImages, setSelectedImages] = useState([]);
const [imagePreviews, setImagePreviews] = useState([]);
const [isLoading, setIsLoading] = useState(false);
const [error, setError] = useState(null);
```

**Key Functions:**

| Function | Purpose |
|----------|---------|
| `handleInputChange()` | Update post fields |
| `handleImagesChange()` | Validate + store images |
| `generatePreview()` | Create thumbnail previews |
| `handleSubmit()` | Create post, upload images |
| `uploadImages()` | POST to `/upload_images/` |

**Validation:**

| Field | Rules |
|-------|-------|
| Images | 1-15 files, ≤5MB each, image/* MIME type |
| Title | Required, ≤100 chars |
| Price | Required, >0 |
| Quantity | Required, >0 |
| Unit | Required |

---

### PostCard.jsx

**Purpose:** Display post with image gallery and modal

**Image Handling:**
```javascript
// Uses images array from PostImageSerializer
// Falls back to legacy image_url for backward compatibility
const images = post.images && post.images.length > 0
  ? post.images.map(img => img.image)
  : post.image_url
    ? [post.image_url]
    : [];
```

**Features:**
- Thumbnail strip (horizontal scroll)
- Full-screen modal
- Arrow key navigation
- Click-outside to close
- Image counter ("1/5")

**State:**
```javascript
const [currentImageIndex, setCurrentImageIndex] = useState(0);
const [isModalOpen, setIsModalOpen] = useState(false);
```

---

## Image Validation

### Frontend Validation (Client-side)

**File:** `components/FarmerPostForm.jsx` (handleImagesChange)

```javascript
if (!file.type.startsWith('image/')) {
  setError('Only image files are allowed');
  return;
}

if (file.size > 5 * 1024 * 1024) {
  setError('Each image must be under 5MB');
  return;
}

if (files.length > 15) {
  setError('Maximum 15 images per post');
  return;
}
```

### Backend Validation (Server-side)

**File:** `posts/validators.py`

```python
def validate_image_file_size(file):
    if file.size > 5 * 1024 * 1024:  # 5MB
        raise ValidationError("Image file too large (max 5MB)")

def validate_image_format(file):
    valid_formats = {'JPEG', 'PNG', 'GIF', 'WEBP'}
    try:
        img = Image.open(file)
        if img.format not in valid_formats:
            raise ValidationError("Invalid image format")
    except Exception:
        raise ValidationError("Invalid image file")
```

**Custom Serializer Validation:**

```python
class PostImageSerializer(serializers.ModelSerializer):
    def validate_image(self, value):
        # Max 15 images per post
        if self.context['request'].method == 'POST':
            post_id = self.context['post_id']
            current_count = PostImage.objects.filter(
                post_id=post_id
            ).count()
            if current_count >= 15:
                raise serializers.ValidationError(
                    "Post already has 15 images"
                )
        return value
```

---

## Error Handling

### Frontend Error States

**In FarmerPostForm:**
```javascript
// File validation errors
if (!file.type.startsWith('image/')) {
  setError('Only image files are allowed');
}

// Submission errors
try {
  await handleSubmit();
} catch (err) {
  setError(err.response?.data?.detail || 'Failed to post');
}

// Display error banner
{error && <div className="error">{error}</div>}
```

### Backend Error Responses

```python
# posts/views.py - upload_images action

if not request.FILES.get('images'):
    return Response(
        {'detail': 'No images provided'},
        status=status.HTTP_400_BAD_REQUEST
    )

if len(files) > 15:
    return Response(
        {'detail': 'Too many images'},
        status=status.HTTP_400_BAD_REQUEST
    )

# Check post ownership
if post.user_id != request.user.id:
    return Response(
        {'detail': 'Permission denied'},
        status=status.HTTP_403_FORBIDDEN
    )
```

---

## Known Limitations

### Current

1. **Batch Upload Only**
   - All images uploaded in single request
   - No progress bar per image
   - If one fails, need to retry all

2. **No Reordering**
   - Images display in upload order (by `order` field)
   - Cannot drag/drop to reorder after upload

3. **No Compression**
   - Pillow validates but doesn't resize
   - Large images consumed at full resolution

4. **No WebP Fallback**
   - Some older browsers may not display WebP
   - Consider jpg/png for max compatibility

### Potential Improvements

- [ ] Individual image upload progress
- [ ] Drag-to-reorder on mobile
- [ ] Auto-resize to max 2000px width
- [ ] Lazy loading gallery thumbnails
- [ ] Image filters/effects (brightness, etc.)
- [ ] Batch delete
- [ ] Image description/alt text per image

---

## Performance Notes

### Image Storage

- **Location:** `MEDIA_ROOT/post_images/` (configurable in settings)
- **Naming:** Original filename preserved
- **Size:** No server-side compression (yet)

### Database Queries

```python
# Efficient query with images included
Post.objects.prefetch_related('images').all()

# Returns: Post with related PostImage objects
# ~1 query per 100 posts (not N+1)
```

### Frontend Performance

- **Gallery modal:** Renders only current image
- **Thumbnail strip:** All loaded (consider virtual scrolling for >50 images)
- **Preview grid:** Only during form (cleared on submit)

---

## Testing Checklist

See [03-TESTING_GUIDE.md](03-TESTING_GUIDE.md) for detailed procedures.

Quick items:
- [ ] Upload 1, 5, 15 images
- [ ] Try 16 images (should fail)
- [ ] Try 10MB file (should fail)
- [ ] Test gallery modal navigation
- [ ] Test on mobile
- [ ] Test permissions (delete other user's images)

---

**Last Updated:** January 10, 2026 | **Status:** Ready for Production
