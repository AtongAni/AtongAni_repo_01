# API Reference

## 📍 All Endpoints

| Method | Endpoint | Status | Notes |
|--------|----------|--------|-------|
| POST | `/api/posts/` | ✅ | Create new post |
| GET | `/api/posts/` | ✅ | List all posts |
| GET | `/api/posts/{id}/` | ✅ | Get post details |
| PUT | `/api/posts/{id}/` | ✅ | Update post |
| DELETE | `/api/posts/{id}/` | ✅ | Delete post |
| **POST** | **`/api/posts/{id}/upload_images/`** | **✅ NEW** | **Upload images (1-15)** |
| **DELETE** | **`/api/posts/{id}/delete_image/{image_id}/`** | **✅ NEW** | **Delete single image** |

---

## 🆕 New Image Endpoints

### Upload Images

**Endpoint:** `POST /api/posts/{post_id}/upload_images/`

**Authentication:** Required (Bearer token or session cookie)

**Purpose:** Upload 1-15 image files to an existing post

**Request Format:**
```
Content-Type: multipart/form-data

Parameters:
  images: File[] (multipart files, 1-15 max)
```

**Request Example (cURL):**
```bash
curl -X POST http://127.0.0.1:8000/api/posts/1/upload_images/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "images=@photo1.jpg" \
  -F "images=@photo2.jpg" \
  -F "images=@photo3.jpg"
```

**Request Example (JavaScript):**
```javascript
const formData = new FormData();
formData.append('images', file1);
formData.append('images', file2);
formData.append('images', file3);

const response = await api.post(
  `/api/posts/${postId}/upload_images/`,
  formData
);
```

**Success Response (201 Created):**
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
    },
    {
      "id": 3,
      "image": "http://127.0.0.1:8000/media/post_images/ghi789.jpg",
      "order": 2,
      "created_at": "2026-01-10T10:30:02Z"
    }
  ]
}
```

**Error Responses:**

| Status | Error Message | Cause | Solution |
|--------|---------------|-------|----------|
| 400 | `"No images provided"` | Request body empty | Attach files to request |
| 400 | `"Too many images"` | More than 15 files | Reduce to 15 or fewer |
| 400 | `"Image file too large"` | File > 5MB | Reduce file size |
| 400 | `"Invalid file format"` | Not an image | Send JPEG/PNG/GIF/WebP |
| 404 | `"Not found"` | Post doesn't exist | Check post ID |
| 403 | `"Permission denied"` | Not post owner | Use your own post |
| 401 | `"Unauthorized"` | Not authenticated | Login first |

---

### Delete Image

**Endpoint:** `DELETE /api/posts/{post_id}/delete_image/{image_id}/`

**Authentication:** Required

**Purpose:** Remove a single image from a post

**Request Format:**
```
No body required
```

**Request Example (cURL):**
```bash
curl -X DELETE http://127.0.0.1:8000/api/posts/1/delete_image/5/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Request Example (JavaScript):**
```javascript
await api.delete(
  `/api/posts/${postId}/delete_image/${imageId}/`
);
```

**Success Response (204 No Content):**
```
[Empty body]
```

**Error Responses:**

| Status | Error | Cause | Solution |
|--------|-------|-------|----------|
| 404 | `"Not found"` | Image doesn't exist | Check image ID |
| 403 | `"Permission denied"` | Not post owner | Must be your post |
| 401 | `"Unauthorized"` | Not authenticated | Login first |

---

## Existing Endpoints (Reference)

### Create Post

**POST** `/api/posts/`

**Request:**
```json
{
  "title": "Fresh Tomatoes",
  "description": "Organic red tomatoes",
  "price": "5.00",
  "quantity": "10",
  "unit": "lbs"
}
```

**Response (201):**
```json
{
  "id": 1,
  "user_id": 5,
  "title": "Fresh Tomatoes",
  "description": "Organic red tomatoes",
  "price": "5.00",
  "quantity": 10,
  "unit": "lbs",
  "created_at": "2026-01-10T10:30:00Z",
  "images": []
}
```

### List Posts

**GET** `/api/posts/`

**Response (200):**
```json
[
  {
    "id": 1,
    "title": "Fresh Tomatoes",
    "price": "5.00",
    "images": [
      {
        "id": 1,
        "image": "http://127.0.0.1:8000/media/post_images/abc123.jpg",
        "order": 0
      }
    ]
  },
  {
    "id": 2,
    "title": "Organic Lettuce",
    "price": "3.00",
    "images": []
  }
]
```

---

## Authentication

All endpoints (except public reads) require:

**Header:**
```
Authorization: Bearer YOUR_JWT_TOKEN
```

**Or:**
```
Cookie: sessionid=YOUR_SESSION_ID
```

### Getting a Token

```bash
# Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"farmer1","password":"pass123"}'

# Response:
{
  "token": "eyJhbGc..."
}
```

---

## Rate Limiting

- **Per endpoint:** No hard limit (configurable in settings)
- **File upload:** Max 15 images per request
- **File size:** Max 5MB per file

---

## Content Types

| Request Type | Header |
|--------------|--------|
| JSON POST | `Content-Type: application/json` |
| File Upload | `Content-Type: multipart/form-data` |
| GET/DELETE | No body required |

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success (GET, PATCH) |
| 201 | Created (POST) |
| 204 | Success with no content (DELETE) |
| 400 | Bad request (validation error) |
| 401 | Unauthorized (not logged in) |
| 403 | Forbidden (no permission) |
| 404 | Not found (resource doesn't exist) |
| 500 | Server error |

---

## Examples

### JavaScript (using axios)

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    Authorization: `Bearer ${localStorage.getItem('token')}`
  }
});

// Create post and upload images
async function createPostWithImages(postData, files) {
  try {
    // Step 1: Create post
    const postResponse = await api.post('/api/posts/', postData);
    const postId = postResponse.data.id;
    
    // Step 2: Upload images
    const formData = new FormData();
    files.forEach(file => formData.append('images', file));
    
    const imageResponse = await api.post(
      `/api/posts/${postId}/upload_images/`,
      formData
    );
    
    console.log('Post created with images:', imageResponse.data);
    return imageResponse.data;
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

// Delete image
async function deleteImage(postId, imageId) {
  try {
    await api.delete(`/api/posts/${postId}/delete_image/${imageId}/`);
    console.log('Image deleted');
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}
```

### Python (using requests)

```python
import requests

BASE_URL = 'http://127.0.0.1:8000'
TOKEN = 'your_jwt_token_here'

headers = {
    'Authorization': f'Bearer {TOKEN}'
}

# Upload images
post_id = 1
files = [
    ('images', open('photo1.jpg', 'rb')),
    ('images', open('photo2.jpg', 'rb')),
    ('images', open('photo3.jpg', 'rb')),
]

response = requests.post(
    f'{BASE_URL}/api/posts/{post_id}/upload_images/',
    files=files,
    headers=headers
)

print(response.json())

# Delete image
image_id = 5
response = requests.delete(
    f'{BASE_URL}/api/posts/{post_id}/delete_image/{image_id}/',
    headers=headers
)

print(response.status_code)
```

---

## Common Errors

### 404 Not Found (Upload)
```json
{
  "detail": "Not found."
}
```
**Cause:** Post ID doesn't exist

**Fix:** Check post ID is correct
```javascript
GET /api/posts/  // List all posts to find correct ID
```

---

### 403 Permission Denied
```json
{
  "detail": "You do not have permission to perform this action."
}
```
**Cause:** Not the post owner

**Fix:** Only owners can upload to their own posts

---

### 400 Too Many Images
```json
{
  "detail": "Too many images. Maximum is 15 per post."
}
```
**Cause:** Sent more than 15 files

**Fix:** Reduce to 15 or fewer files
```javascript
const files = selectedFiles.slice(0, 15);
```

---

### 400 File Too Large
```json
{
  "detail": "Image file too large (max 5MB)"
}
```
**Cause:** File exceeds 5MB

**Fix:** Compress image or use smaller file
```javascript
if (file.size > 5 * 1024 * 1024) {
  console.log('File too large');
}
```

---

## Testing

### cURL Examples

**Upload 3 images:**
```bash
curl -X POST http://127.0.0.1:8000/api/posts/1/upload_images/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "images=@/path/to/photo1.jpg" \
  -F "images=@/path/to/photo2.jpg" \
  -F "images=@/path/to/photo3.jpg"
```

**Delete image:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/posts/1/delete_image/5/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Get post with images:**
```bash
curl http://127.0.0.1:8000/api/posts/1/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Need Help?

- **Feature Overview:** See [../FEATURES/multi-image-posts/01-QUICK_START.md](../FEATURES/multi-image-posts/01-QUICK_START.md)
- **Technical Deep Dive:** See [../FEATURES/multi-image-posts/02-TECHNICAL_REFERENCE.md](../FEATURES/multi-image-posts/02-TECHNICAL_REFERENCE.md)
- **Testing:** See [../FEATURES/multi-image-posts/03-TESTING_GUIDE.md](../FEATURES/multi-image-posts/03-TESTING_GUIDE.md)

---

**Last Updated:** January 10, 2026 | **API Version:** 1.0.0
