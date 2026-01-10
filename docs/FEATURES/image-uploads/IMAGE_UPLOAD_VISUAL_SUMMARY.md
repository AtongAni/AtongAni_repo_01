# Image Upload Feature - Visual Summary

## What Was Built

```
┌─────────────────────────────────────────────────────────────┐
│                   FARMERS MARKET APP                        │
│                  Image Upload Feature                       │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ FARMER CREATES POST                                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Create a New Post                                   │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ Title *        [What are you selling?................] │   │
│  │ Description *  [Describe your product................ │   │
│  │                ...............................]      │   │
│  │ Product Image  [Choose File]               [No file] │   │
│  │                Formats: JPEG, PNG, GIF, WebP (5MB)  │   │
│  │                                                      │   │
│  │                ┌──────────────────────┐             │   │
│  │                │    [Preview Image]   │             │   │
│  │                │   200x200 (optional) │             │   │
│  │                │  [Remove Image] btn  │             │   │
│  │                └──────────────────────┘             │   │
│  │                                                      │   │
│  │ Price (₱ PHP)  [50.00..............]                │   │
│  │ Available Qty  [100........] Unit [KG ▼]           │   │
│  │                                                      │   │
│  │                         [POST] button               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ DATA FLOW                                                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Frontend                Backend                Database     │
│  ─────────                ───────                ────────    │
│                                                              │
│  Select Image ──┐                                          │
│  (JPEG/PNG)    │                                            │
│                │  FormData (multipart/form-data)           │
│  Show Preview  │  ────────────────────────────────>        │
│                │                                 │          │
│  Validate      │  Django Serializer             │          │
│  (Size < 5MB)  │  ├─ Validate file type  ✓     │          │
│                │  ├─ Validate file size  ✓     │          │
│                │  │                             │          │
│  User clicks   │  └─> Save to media/posts/ ────┼────>     │
│  POST button   │      abc123.jpg                │          │
│                │                                 │          │
│  Return        │  Store path in DB:            │          │
│  image_url     │  "posts/abc123.jpg"            │          │
│  <──────────────  and return response ──────────┘          │
│                                                              │
│  Display image                                              │
│  in post card                                               │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ POST FEED DISPLAY                                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 🟢 John Doe                    ₱ 50.00              │  │
│  │    2024-01-10                                       │  │
│  │  ┌──────────────────────────────────────────────────┐│  │
│  │  │ Fresh Organic Tomatoes                          ││  │
│  │  │                                                  ││  │
│  │  │ Pesticide-free, locally grown tomatoes...       ││  │
│  │  │                                                  ││  │
│  │  │            ┌────────────────────┐               ││  │
│  │  │            │   Product Image    │  ← NEW!      ││  │
│  │  │            │   (200px height)   │               ││  │
│  │  │            │   Responsive       │               ││  │
│  │  │            └────────────────────┘               ││  │
│  │  │                                                  ││  │
│  │  │ Available: 100 kg                               ││  │
│  │  └──────────────────────────────────────────────────┘│  │
│  │  💬 Comment    🛒 Add to Cart    🗑️ Delete        │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ STORAGE STRUCTURE                                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  farmers-market/                                            │
│  │                                                          │
│  ├── media/                          ← NEW!                │
│  │   └── posts/                      ← Image folder       │
│  │       ├── post_1_img_abc123.jpg                        │
│  │       ├── post_2_img_xyz789.png                        │
│  │       └── ...                                          │
│  │                                                          │
│  ├── posts/                                                │
│  │   ├── migrations/                                       │
│  │   │   └── 0003_alter_post_image.py   ← NEW migration  │
│  │   ├── models.py                       ← UPDATED        │
│  │   └── serializers.py                  ← UPDATED        │
│  │                                                          │
│  ├── config/                                               │
│  │   ├── settings.py                     ← UPDATED        │
│  │   └── urls.py                         ← UPDATED        │
│  │                                                          │
│  └── requirements.txt                    ← NEW!            │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ DATABASE SCHEMA - POST TABLE                                 │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  id (PK)         │  title          │  content              │
│  ─────────────────────────────────────────────              │
│  1               │  Fresh Tomato   │  Organic, pesticide.. │
│  2               │  Fresh Lettuce  │  Crispy, fresh....    │
│                                                              │
│  author_id       │  image          │  image_url (API)      │
│  ──────────────────────────────────────────────             │
│  5 (Farmer)      │  posts/abc123   │  /media/posts/abc123  │
│  6 (Farmer)      │  posts/xyz789   │  /media/posts/xyz789  │
│                                                              │
│  Each image is linked to:                                   │
│  • The post (directly via image field)                      │
│  • The farmer (via author_id foreign key)                   │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ API RESPONSE EXAMPLE                                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  GET /api/posts/                                            │
│                                                              │
│  {                                                          │
│    "id": 1,                                                │
│    "author": {                                             │
│      "id": 5,                                              │
│      "username": "farmer_john",                            │
│      "first_name": "John",                                 │
│      "last_name": "Doe"                                    │
│    },                                                       │
│    "author_id": 5,  ← Links to farmer                      │
│    "title": "Fresh Organic Tomatoes",                      │
│    "content": "Pesticide-free...",                         │
│    "image": "posts/post_1_abc123.jpg",    ← Path stored   │
│    "image_url": "http://localhost:8000/media/posts/...",   │
│    "price": "50.00",                                       │
│    "quantity": "100.00",                                   │
│    "unit": "KG",                                           │
│    "created_at": "2024-01-10T10:30:00Z",                  │
│    "updated_at": "2024-01-10T10:30:00Z"                   │
│  }                                                          │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ VALIDATION FLOW                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  User selects file                                          │
│         │                                                   │
│         ├─→ CLIENT-SIDE VALIDATION (FarmerPostForm)       │
│         │                                                   │
│         │   ✓ Is file type JPEG/PNG/GIF/WebP?             │
│         │   ✓ Is file size < 5MB?                         │
│         │   ✓ Show preview (FileReader API)               │
│         │                                                   │
│         ├─→ Form submission with FormData                 │
│         │                                                   │
│         ├─→ BACKEND VALIDATION (Serializer)               │
│         │                                                   │
│         │   ✓ MIME type check (security)                  │
│         │   ✓ File size check (5MB limit)                 │
│         │   ✓ All required fields present                 │
│         │                                                   │
│         └─→ Save and return response                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ FEATURE CHECKLIST                                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  [✓] Farmers can upload images when creating posts         │
│  [✓] Images stored in media/posts/ folder                  │
│  [✓] Database stores file path with post                   │
│  [✓] Images linked to both post and farmer                 │
│  [✓] Client-side validation (type, size)                   │
│  [✓] Server-side validation (security)                     │
│  [✓] Real-time preview before posting                      │
│  [✓] Clear/remove image button                             │
│  [✓] Images display in post feed                           │
│  [✓] Responsive image sizing                               │
│  [✓] Error messages for invalid files                      │
│  [✓] Optional image (can post without)                     │
│  [✓] Safe filename generation                              │
│  [✓] Full URL returned in API                              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Key Implementation Facts

| Aspect | Details |
|--------|---------|
| **Storage** | `media/posts/` folder (auto-created on first upload) |
| **File Format** | JPEG, PNG, GIF, WebP (validated on both frontend and backend) |
| **File Size Limit** | 5MB maximum |
| **Database Field** | `ImageField` (stores relative path like "posts/abc123.jpg") |
| **API Response** | Returns both `image` (path) and `image_url` (full URL) |
| **Image-to-Post Link** | Direct ImageField on Post model |
| **Image-to-Farmer Link** | Through `author` ForeignKey on Post model |
| **Optional** | Yes - posts can be created without images |
| **Display** | 200px max height, responsive width |

## Quick Start

```bash
# 1. Install Pillow
pip install Pillow

# 2. Run migration
python manage.py migrate posts

# 3. Start server
python manage.py runserver

# 4. Test in browser at http://localhost:3000
```

That's it! The feature is ready to use. 🎉
