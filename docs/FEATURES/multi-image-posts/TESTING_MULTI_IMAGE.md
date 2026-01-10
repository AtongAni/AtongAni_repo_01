# Multi-Image Feature - Quick Testing Guide

## Prerequisites
- ✅ Database migration run: `python manage.py migrate posts`
- ✅ Django server running: `python manage.py runserver`
- ✅ React dev server running: `npm run dev` (in web/ directory)

## Testing Steps

### 1. Create a Post with Multiple Images

**In the App:**
1. Navigate to Dashboard/Posts section
2. Click "Create a New Post" form
3. Fill in:
   - Title: "Fresh Organic Tomatoes"
   - Description: "Delicious locally-grown tomatoes, perfect for salads and cooking"
   - Price: 150.00
   - Quantity: 50
   - Unit: KG

4. **Select Images:**
   - Click "Product Images" input field
   - Select 3-5 image files at once (JPEG, PNG, GIF, or WebP)
   - Verify preview grid appears with thumbnails
   - Verify counter shows: "3/15 images selected"
   - Remove one image by clicking the ✕ button
   - Verify counter updates: "2/15 images selected"

5. **Submit:**
   - Click "Post" button
   - Verify button shows "Creating post..." briefly
   - Verify button changes to "Uploading images..."
   - Verify success message: "Post created successfully!"
   - Verify form resets

### 2. View Post with Multiple Images

**In the Feed:**
1. Scroll to find your newly created post
2. **Verify Display:**
   - Title and description visible
   - Main image displayed with full aspect ratio
   - Image counter visible: "1/2" (if 2 images)
   - "Click to view" hint appears on hover
   
3. **Gallery Thumbnails:**
   - Verify horizontal scrollable strip appears with 60x60px thumbnails
   - Verify first thumbnail is highlighted (green border)
   - Click second thumbnail
   - Verify main image changes to second image
   - Verify counter updates: "2/2"

### 3. Open Full-Screen Modal

1. **Click on Image:**
   - Click main image to open modal
   - Verify full-screen overlay appears with dark background
   - Verify image displayed at larger size
   - Verify close button (✕) in top-right
   - Verify product info visible below image

2. **Navigation (if multiple images):**
   - Verify navigation arrows appear (❮ ❯)
   - Click right arrow (❯)
   - Verify image changes and counter updates: "2/2"
   - Click left arrow (❮)
   - Verify image changes back: "1/2"
   - Verify arrows wrap around (at last image, next goes to first)

3. **Close Modal:**
   - Click ✕ button
   - Verify modal closes
   - Verify back in main feed

### 4. Test Edge Cases

#### A. Maximum Images (15)
1. Create post and select 15 images
2. Try to add one more file
3. Verify error: "Maximum 15 images allowed..."

#### B. File Size Validation
1. Create post and try to upload file > 5MB
2. Verify error: "[filename] is too large (max 5MB)"

#### C. Invalid Format
1. Try to upload .txt, .pdf, or other non-image file
2. Verify error: "[filename] has unsupported format. Allowed: JPEG, PNG, GIF, WebP"

#### D. No Images
1. Create post with 0 images
2. Verify post created successfully
3. Verify no image section in feed
4. Verify post otherwise displays normally

#### E. Legacy Single Image Post
1. Check older posts created before multi-image feature
2. Verify they still display with single image
3. Verify gallery strip not shown (only 1 image)
4. Verify modal still works for zooming

### 5. Delete Images

**If ownership:**
1. View own post in feed
2. Verify "Delete" button visible
3. Click "Delete"
4. Verify confirmation modal
5. Click "Delete" in confirmation
6. Verify post and all images deleted
7. Verify post removed from feed

### 6. Mobile Responsiveness

**On Mobile/Tablet:**
1. Open app on smaller screen
2. Verify image preview grid is responsive (fewer columns on narrow screens)
3. Verify thumbnail gallery still scrollable
4. Verify modal fits screen
5. Verify buttons are touch-friendly size (44px minimum)
6. Verify no horizontal overflow

## API Testing (Using curl or Postman)

### Create Post
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "title=Test Post" \
  -F "content=Test Description" \
  -F "price=100" \
  -F "quantity=10" \
  -F "unit=KG"
```

### Upload Images
```bash
curl -X POST http://localhost:8000/api/posts/1/upload_images/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "images=@image1.jpg" \
  -F "images=@image2.jpg" \
  -F "images=@image3.jpg"
```

### Response (Success)
```json
{
  "success": true,
  "images": [
    {
      "id": 101,
      "image_url": "http://localhost:8000/media/posts/image1.jpg",
      "order": 0,
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": 102,
      "image_url": "http://localhost:8000/media/posts/image2.jpg",
      "order": 1,
      "created_at": "2024-01-15T10:30:01Z"
    }
  ],
  "errors": []
}
```

### Delete Image
```bash
curl -X DELETE http://localhost:8000/api/posts/1/delete_image/?image_id=101 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Expected Behaviors

### Form Submission
- ✅ Post created even if no images selected
- ✅ Images uploaded only if they exist
- ✅ Error shown if image upload fails (but post still exists)
- ✅ Form clears after successful submission
- ✅ Success message displays for 1.5 seconds

### Gallery Display
- ✅ Gallery thumbnails only shown if multiple images
- ✅ Current image highlighted in gallery
- ✅ Counter only shown if multiple images
- ✅ Single-image posts display normally without gallery

### Modal Navigation
- ✅ Navigation arrows only shown if multiple images
- ✅ Arrows wrap around (last → first, first → previous)
- ✅ Counter updates as images change
- ✅ Clicking outside modal closes it
- ✅ ✕ button closes modal

### Validation
- ✅ Title required
- ✅ Description required
- ✅ Price/quantity optional
- ✅ Images optional
- ✅ File size checked (5MB max)
- ✅ File format validated
- ✅ Total image count limited (15 max)
- ✅ Feedback for all errors

### Ownership
- ✅ Only post author can delete
- ✅ Only post author can add images
- ✅ Other users can view images
- ✅ Other users can add to cart

## Browser Developer Tools

### Check Network Requests
1. Open DevTools (F12)
2. Go to Network tab
3. Create new post with images
4. Verify requests:
   - `POST /api/posts/` - Create post
   - `POST /api/posts/{id}/upload_images/` - Upload images
5. Check response bodies for `images` array

### Check Console
1. Open DevTools Console tab
2. Create post with images
3. Verify no JavaScript errors
4. Verify no network errors (404, 500, etc.)

### Check Application/Storage
1. Go to Application tab
2. Check localStorage for any relevant data
3. Clear cache if images not updating

## Troubleshooting

### Images Not Showing
1. Check Django console for errors
2. Verify files uploaded to `farmers-market/media/posts/`
3. Check image URLs in browser DevTools Network tab
4. Try hard refresh (Ctrl+Shift+R)

### Form Not Submitting
1. Check browser console for JavaScript errors
2. Verify API endpoints accessible
3. Verify authentication token valid
4. Check Django logs

### Images Not Uploading to Database
1. Run `python manage.py migrate posts` if not done
2. Check Django logs for validation errors
3. Verify `MEDIA_ROOT` setting in settings.py
4. Verify permissions on `media/` directory

### Modal Not Opening
1. Check browser console for errors
2. Verify image URLs valid (200 status in Network tab)
3. Try different browser/clear cache
4. Check CSS z-index values (should be 1000+)

## Files Modified

### Backend
- ✅ `farmers-market/posts/models.py` - Added PostImage model
- ✅ `farmers-market/posts/migrations/0004_postimage.py` - Created migration
- ✅ `farmers-market/posts/serializers.py` - Added PostImageSerializer, updated PostSerializer
- ✅ `farmers-market/posts/views.py` - Added upload_images and delete_image actions

### Frontend
- ✅ `web/src/components/FarmerPostForm.jsx` - Rewrote for multi-image support
- ✅ `web/src/components/FarmerPostForm.css` - Added gallery grid styles
- ✅ `web/src/components/PostCard.jsx` - Added gallery thumbnails and image navigation
- ✅ `web/src/components/PostCard.css` - Added gallery and modal navigation styles
- ✅ `web/src/api/posts.js` - Added uploadPostImages and deletePostImage functions

## Success Indicators

### When Everything Works:
1. ✅ Can create post with 0-15 images
2. ✅ Images display in gallery on feed
3. ✅ Thumbnails clickable to switch images
4. ✅ Modal opens with full-size image
5. ✅ Navigation arrows cycle through images
6. ✅ Counter shows current position
7. ✅ Validation prevents invalid files
8. ✅ Error messages clear and helpful
9. ✅ Mobile layout responsive
10. ✅ Legacy posts still work

## Performance Notes

- Form submission takes ~1-2 seconds for post creation
- Image upload takes ~1-5 seconds depending on file sizes and network
- Gallery rendering instant (images preloaded in HTTP response)
- Modal opening/closing smooth with animations
- Navigation arrows responsive to clicks

## Support / Questions

Refer to `MULTI_IMAGE_FEATURE.md` for detailed documentation on:
- Architecture and database design
- API endpoint specifications
- Validation rules
- Future enhancements
- Troubleshooting guide
