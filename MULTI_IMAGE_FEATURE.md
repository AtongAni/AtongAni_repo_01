# Multi-Image Feature Implementation

## Overview
The farmers market application now supports uploading up to **15 images per post**, enabling farmers to showcase their products from multiple angles and provide better product visibility.

## Architecture

### Database Schema

#### PostImage Model
```python
class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
```

**Fields:**
- `post`: ForeignKey to Post (images are deleted when post is deleted)
- `image`: ImageField storing the image file in `media/posts/`
- `order`: Integer for gallery sequencing
- `created_at`: Timestamp for tracking upload time

**Backward Compatibility:**
- Original `Post.image` field (single image) still exists
- Serializer checks `images` relationship first, falls back to legacy `image` field
- Existing posts with single images continue to work

### API Endpoints

#### Create Post (Unchanged)
```
POST /api/posts/
```
Creates post without images. Images uploaded separately afterward.

**Payload:**
```json
{
  "title": "Fresh Tomatoes",
  "content": "Locally grown organic tomatoes",
  "price": 150.00,
  "quantity": 50,
  "unit": "KG"
}
```

#### Upload Images (New)
```
POST /api/posts/{id}/upload_images/
Content-Type: multipart/form-data
```

**Validation:**
- Maximum 15 images total per post
- Maximum 5MB per image file
- Allowed formats: JPEG, PNG, GIF, WebP
- Returns created PostImage records with full URLs

**Request:**
```
Form Data:
- images: [File1, File2, ..., FileN]
```

**Response:**
```json
{
  "success": true,
  "images": [
    {
      "id": 1,
      "image_url": "http://localhost:8000/media/posts/img1.jpg",
      "order": 0,
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": 2,
      "image_url": "http://localhost:8000/media/posts/img2.jpg",
      "order": 1,
      "created_at": "2024-01-15T10:30:01Z"
    }
  ],
  "errors": []
}
```

#### Delete Image (New)
```
DELETE /api/posts/{postId}/delete_image/?image_id={imageId}
```

**Validation:**
- Only post author can delete images
- Image must belong to the specified post

**Response:**
```json
{
  "message": "Image deleted successfully"
}
```

### Serializers

#### PostImageSerializer
```python
class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'image_url', 'order', 'created_at']
    
    def get_image_url(self, obj):
        return obj.image.url if obj.image else None
```

#### PostSerializer (Updated)
```python
class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'price', 'quantity', 'unit', 'images', 'image_url', ...]
    
    def get_image_url(self, obj):
        # Check new images first, fallback to legacy single image
        if obj.images.exists():
            return obj.images.first().image.url
        return obj.image.url if obj.image else None
```

## Frontend Components

### FarmerPostForm.jsx

#### State Management
```javascript
const [images, setImages] = useState([]); // Array of {id, file, preview, uploaded}
const [createdPostId, setCreatedPostId] = useState(null);
const [uploading, setUploading] = useState(false);
```

#### Two-Step Submission Process

**Step 1: Create Post**
- Validates title and description
- Submits post without images
- Receives `postId` in response

**Step 2: Upload Images**
- Sends images to `/api/posts/{postId}/upload_images/`
- Called only if images exist
- Updates UI with upload progress

**Code Flow:**
```javascript
async function handleSubmit(e) {
  // 1. Create post
  const postResponse = await createPost(formData);
  const postId = postResponse.id;
  
  // 2. Upload images if any
  if (images.length > 0) {
    await uploadImages(postId);
  }
  
  // 3. Show success and reset
}
```

#### Image Handling Functions

**handleImagesChange(e)**
- Accepts multiple files at once
- Validates each file (size, format)
- Enforces 15 image maximum
- Generates base64 previews for local display
- Assigns unique IDs for removal tracking

**removeImage(imageId)**
- Removes image from local state before upload
- Updates preview grid in real-time

**uploadImages(postId)**
- Called after post creation
- Sends files to API endpoint
- Marks images as uploaded in state
- Handles upload errors

#### UI Elements

**Image Input:**
- Multi-file input with `accept="image/jpeg,image/png,image/gif,image/webp"`
- Disabled when 15 images selected
- Counter display: "X/15 images selected"

**Preview Grid:**
- CSS Grid layout: 4 columns on desktop, responsive on mobile
- 100x100px thumbnails with aspect ratio
- Hover effects for better UX
- Remove button (✕) on each thumbnail
- "Uploaded" badge for successful uploads

**Help Text:**
```
Supported formats: JPEG, PNG, GIF, WebP (max 5MB each)
5/15 images selected
```

**Button States:**
```
"Creating post..." - During post submission
"Uploading images..." - During image upload
"Post" - Ready to submit
(disabled) - When loading or uploading
```

### PostCard.jsx

#### Multi-Image Display

**Images Array Management:**
```javascript
const images = post?.images && post.images.length > 0 
  ? post.images 
  : post?.image_url ? [{ id: 'legacy', image_url: post.image_url }] : [];
```
- Uses new `images` relationship if available
- Falls back to legacy `image_url` for backward compatibility
- Handles posts with no images gracefully

#### Gallery Thumbnail Strip

**Visible when multiple images exist:**
- Horizontal scrollable strip below title
- 60x60px thumbnails with rounded corners
- Active thumbnail highlighted with green border
- Click to select image (updates main display)
- Responsive: hidden on narrow screens if needed

**CSS:**
```css
.post-image-gallery {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding: 12px 16px;
}

.gallery-thumbnail {
  width: 60px;
  height: 60px;
  flex-shrink: 0;
  border: 2px solid transparent;
  border-radius: 4px;
  cursor: pointer;
}

.gallery-thumbnail.active {
  border-color: #4caf50;
}
```

#### Main Image Display

**Features:**
- Shows currently selected image
- Max height: 400px, maintains aspect ratio
- Image counter in top-left: "2/5"
- "Click to view" hint on hover
- Click opens modal with full-size view

**Backward Compatibility:**
- Single-image posts show 1 thumbnail in gallery
- No gallery strip displayed if only 1 image
- Counter hidden if only 1 image

#### Image Modal

**Enhanced Features:**
- Navigation arrows (❮ ❯) appear when multiple images
- Arrow buttons on left and right sides
- Click arrows to cycle through images
- Image counter: "Image 2 of 5"
- Same product info display below image

**Navigation Logic:**
```javascript
// Next button
() => setCurrentImageIndex((prev) => 
  prev === images.length - 1 ? 0 : prev + 1
)

// Wraps around: last → first, first → previous
```

**Modal Styling:**
- Full-screen overlay
- Image centered with max 60vh height
- Product info panel below (30vh max, scrollable)
- Close button (✕) in top-right
- Dark background (0.85 opacity)

## Client Validation

### File Validation Rules
- **Size**: Maximum 5MB per file
- **Format**: JPEG, PNG, GIF, WebP only
- **Count**: Maximum 15 per post
- **Error Messages**: Clear feedback for each violation

### Example Error Handling
```javascript
if (file.size > 5 * 1024 * 1024) {
  setError(`"${file.name}" is too large (max 5MB).`);
}

const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
if (!allowedTypes.includes(file.type)) {
  setError(`"${file.name}" has unsupported format...`);
}

if (totalImages > 15) {
  setError(`Maximum 15 images allowed. You have ${images.length}...`);
}
```

## Server Validation

### Backend Validation (views.py)

**File Validation:**
```python
ALLOWED_MIMETYPES = [
    'image/jpeg', 'image/png', 'image/gif', 'image/webp'
]
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

for file in files:
    if file.size > MAX_FILE_SIZE:
        errors.append(f"{file.name}: File too large")
    if file.content_type not in ALLOWED_MIMETYPES:
        errors.append(f"{file.name}: Unsupported format")
```

**Image Count Validation:**
```python
current_count = post.images.count()
if current_count + len(files) > 15:
    return Response(
        {'error': f'Maximum 15 images allowed...'},
        status=status.HTTP_400_BAD_REQUEST
    )
```

**Ownership Validation:**
```python
if post.author != request.user:
    return Response(
        {'error': 'You can only add images to your own posts'},
        status=status.HTTP_403_FORBIDDEN
    )
```

## Database Migrations

### Migration 0004_postimage.py
- Creates `posts_postimage` table
- Adds ForeignKey to Post
- Sets up `order` field for sequencing
- Adds indexes for efficient querying

**Run Migration:**
```bash
python manage.py migrate posts
```

**Verify Migration:**
```bash
python manage.py showmigrations posts
```

## User Workflow

### Creating a Post with Multiple Images

1. **Fill Post Details**
   - Enter title, description, price, quantity
   - Select unit of measurement

2. **Select Images**
   - Click "Product Images" input
   - Select multiple image files at once
   - Images appear in preview grid below input
   - Counter shows progress: "3/15 images selected"

3. **Manage Images**
   - Remove images by clicking ✕ button
   - Reorder by removing and re-adding (or use drag-and-drop in future)
   - Previews update in real-time

4. **Submit**
   - Click "Post" button
   - Form validates (title, description required)
   - Post created first (shows "Creating post...")
   - Images uploaded in second step (shows "Uploading images...")
   - Success message: "Post created successfully!"
   - Form resets for new post

### Viewing a Post

1. **Main Feed**
   - Single image displayed with full aspect ratio
   - If multiple images, thumbnail gallery appears below
   - Click thumbnail to select different image
   - "Click to view" hint appears on hover

2. **Image Modal**
   - Click image to open full-screen modal
   - Navigate with arrows if multiple images
   - Image counter shows position: "2 of 5"
   - Product details visible below image
   - Click anywhere outside modal or ✕ to close

### Managing Images (Post Owner)

1. **View Own Post**
   - Same display as other users

2. **Delete Post**
   - Click "Delete" button
   - Confirm deletion
   - Post and all images deleted together

## Backward Compatibility

### Legacy Posts (Single Image)
- Existing posts with `Post.image` field continue to work
- Treated as `images[0]` in serializer response
- No migration needed for existing posts
- Can add more images to legacy posts

### API Response for Legacy Post
```json
{
  "id": 1,
  "title": "Legacy Post",
  "image_url": "http://...legacy-image.jpg",
  "images": [
    {
      "id": 101,
      "image_url": "http://...legacy-image.jpg",
      "order": 0
    }
  ]
}
```

## Performance Considerations

### Database Queries
- Use `select_related()` for author in PostSerializer
- Use `prefetch_related()` for images relationship
- Indexes on `post_id` and `order` fields

### Image Optimization
- Pillow validates images on upload
- Client-side preview generation (doesn't upload)
- Sequential upload (could be optimized to parallel in future)

### Storage
- Images stored in `media/posts/` directory
- Original filenames preserved with UUID prefix
- Organized by upload date subdirectories (future enhancement)

## Testing Scenarios

### Happy Path
- [ ] Create post with 0 images
- [ ] Create post with 1 image
- [ ] Create post with 5 images
- [ ] Create post with 15 images (maximum)
- [ ] View images in gallery
- [ ] Click image to open modal
- [ ] Navigate images in modal with arrows
- [ ] Delete post with images

### Edge Cases
- [ ] Try to upload 16 images (should reject)
- [ ] Try to upload file > 5MB (should show error)
- [ ] Try to upload unsupported format (should show error)
- [ ] Remove all images from preview before submitting
- [ ] Fail image upload after post created (shows error but post exists)
- [ ] Attempt to edit/delete images on others' posts (should reject)

### Mobile
- [ ] Thumbnail gallery scrollable on narrow screens
- [ ] Modal fits screen on mobile
- [ ] Image preview grid responsive on mobile
- [ ] Touch-friendly button sizes (44px minimum)

## Future Enhancements

### Potential Improvements
1. **Drag-and-Drop**
   - Reorder images in preview grid
   - Drag files directly to upload area

2. **Image Editing**
   - Crop/rotate before upload
   - Client-side image optimization

3. **Parallel Upload**
   - Upload multiple images simultaneously
   - Progress bar per image

4. **Image Gallery Features**
   - Infinite scroll carousel
   - Swipe navigation on mobile
   - Keyboard shortcuts (← →) in modal

5. **Image Optimization**
   - Server-side resizing for thumbnails
   - WebP conversion for better compression
   - Lazy loading for large galleries

6. **Analytics**
   - Track which images are most viewed
   - Average time spent per image

## Troubleshooting

### Images Not Uploading
1. Check file size (max 5MB)
2. Verify file format (JPEG, PNG, GIF, WebP)
3. Check `media/` directory permissions
4. Verify Django `MEDIA_URL` and `MEDIA_ROOT` settings

### Images Not Displaying
1. Verify full URL in response includes `http://`
2. Check `MEDIA_ROOT` directory exists
3. Verify files uploaded to correct location
4. Check browser console for 404 errors

### Database Migration Errors
```bash
# Reset migrations (development only)
python manage.py migrate posts zero
python manage.py migrate posts
```

### API Errors
- 403: Not post author (can't upload/delete)
- 400: File validation failed or max images exceeded
- 404: Post or image not found
- 500: Server error (check Django logs)

## API Client Functions

### uploadPostImages(postId, files)
```javascript
import { uploadPostImages } from "../api/posts";

await uploadPostImages(123, [file1, file2, file3]);
// Returns: { success, images, errors }
```

### deletePostImage(postId, imageId)
```javascript
import { deletePostImage } from "../api/posts";

await deletePostImage(123, 456);
// Returns: { message: "Image deleted successfully" }
```

## Summary

The multi-image feature provides:
- ✅ Up to 15 images per post
- ✅ Client and server-side validation
- ✅ Real-time preview feedback
- ✅ Image gallery with navigation
- ✅ Full-screen modal viewing
- ✅ Backward compatibility
- ✅ Mobile-responsive design
- ✅ Secure ownership validation

This enhancement significantly improves the farmer marketplace experience by allowing comprehensive product showcase with multiple perspectives.
