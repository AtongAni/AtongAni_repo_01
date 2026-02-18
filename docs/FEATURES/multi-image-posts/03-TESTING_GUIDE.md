# Multi-Image Posts - Testing Guide

**Status:** Ready for QA | **Version:** 1.0.0

---

## 🧪 Test Execution Plan

### Test Environment Setup

**Prerequisites:**
```
✅ Backend: python manage.py runserver
✅ Frontend: npm run dev (from web/)
✅ Database: Migration 0004_postimage executed
✅ User account: Created and logged in
```

**Verify Setup:**
1. Open DevTools → Network tab (watch API calls)
2. Open DevTools → Console tab (check for errors)
3. Check MEDIA_ROOT folder exists: `farmers-market/media/post_images/`

---

## 🎯 Test Scenarios

### Scenario 1: Basic Upload (Happy Path)

**Goal:** Create post with 3 images successfully

**Steps:**
1. Navigate to "New Post" form
2. Fill in:
   - Title: "Fresh Tomatoes"
   - Description: "Organic red tomatoes"
   - Price: "$5.00"
   - Quantity: "10"
   - Unit: "lbs"
3. Click "Product Images"
4. Select 3 image files (JPEG/PNG, each <5MB)
5. Verify preview grid shows all 3 images
6. Click "Post" button
7. Wait for upload to complete

**Expected Results:**
- ✅ POST `/api/posts/` → 201 Created
- ✅ GET postId from response
- ✅ POST `/api/posts/{id}/upload_images/` → 201 Created
- ✅ Page redirects to Dashboard
- ✅ New post appears in feed with gallery
- ✅ Gallery shows 3 thumbnail images
- ✅ No errors in console

**Files Created:**
- `media/post_images/{uuid}.jpg` (×3)
- Database rows: 1 Post + 3 PostImage rows

**Cleanup:**
- Delete post from Admin (cascade deletes PostImage rows and files)

---

### Scenario 2: Maximum Images (Edge Case)

**Goal:** Verify 15-image limit enforced

**Test 2a: Exactly 15 Images**
1. Create post with **exactly 15 images**
2. Submit form
3. ✅ Should succeed
4. Verify in feed that all 15 thumbnails display

**Test 2b: 16 Images (Over Limit)**
1. In form, select 16 image files
2. Try to submit
3. ✅ Should show error: "Maximum 15 images per post"
4. Form should not submit
5. Can still edit and reduce to 15

---

### Scenario 3: Image Size Validation

**Goal:** Verify file size limits

**Test 3a: Exactly 5MB (Max Allowed)**
1. Create image file exactly 5MB (e.g., solid color 2000×2000px JPEG)
2. Add to post form
3. ✅ Should accept (preview shows)
4. Submit should work

**Test 3b: 5.1MB (Over Limit)**
1. Create image file 5.1MB
2. Add to post form
3. ✅ Should show error: "Each image must be under 5MB"
4. File should not appear in preview
5. Can add different image

---

### Scenario 4: Image Format Validation

**Goal:** Verify only image files accepted

**Test 4a: Valid Formats**

Test each format:
```
✅ JPEG (.jpg, .jpeg)
✅ PNG (.png)
✅ GIF (.gif)
✅ WebP (.webp)
```

Steps:
1. Select one file of each type
2. All should appear in preview grid
3. Submit succeeds
4. All images save to database

**Test 4b: Invalid Formats**

Test each format (should fail):
```
❌ PDF (.pdf)
❌ Word (.docx)
❌ Text (.txt)
❌ SVG (.svg)
❌ HTML (.html)
```

Steps:
1. Try to select invalid file
2. ✅ Should show error: "Only image files are allowed"
3. File not added to preview
4. Can select valid file instead

---

### Scenario 5: Gallery Display & Navigation

**Goal:** Verify image gallery UI works correctly

**Test 5a: Thumbnail Strip**
1. Create post with 5 images
2. View in feed
3. ✅ First image displays large
4. ✅ 5 thumbnail squares visible below/beside
5. ✅ Image counter shows "1/5"

**Test 5b: Click to Switch**
1. Click 3rd thumbnail
2. ✅ Large image updates to 3rd image
3. ✅ Counter changes to "3/5"
4. ✅ 3rd thumbnail highlighted

**Test 5c: Full-Screen Modal**
1. Click large image to open modal
2. ✅ Full-screen modal appears
3. ✅ Image shown at max size
4. ✅ Navigation arrows visible
5. ✅ Image counter shows "3/5"
6. ✅ Close button (×) visible

**Test 5d: Arrow Navigation**
1. In modal, click right arrow
2. ✅ Image advances to 4/5
3. ✅ Click right again → 5/5
4. ✅ Click right at end → wraps to 1/5 (or stops)
5. ✅ Click left → goes back
6. ✅ Keyboard arrows work (if implemented)

**Test 5e: Close Modal**
1. Click × button
2. ✅ Modal closes
3. ✅ Back in feed view
4. ✅ Gallery still visible

---

### Scenario 6: Mobile Responsiveness

**Goal:** Verify feature works on mobile devices

**Test Environment:**
```
Device 1: iPhone 13 (375px width)
Device 2: iPad (768px width)
Device 3: Android phone (412px width)
```

**Test 6a: Form on Mobile**
1. Open "New Post" form on mobile
2. ✅ Images input visible
3. ✅ Preview grid stacks vertically
4. ✅ All images visible without horizontal scroll
5. ✅ Can select images from phone gallery
6. ✅ Submit button accessible

**Test 6b: Gallery on Mobile**
1. View post with 5 images on mobile
2. ✅ First image full-width
3. ✅ Thumbnail strip scrollable horizontally
4. ✅ Touch to switch images works
5. ✅ Modal displays full-screen
6. ✅ Swipe to navigate (if implemented)

**Test 6c: Modal on Mobile**
1. Open full-screen modal on mobile
2. ✅ Image fills screen width
3. ✅ Navigation arrows visible and tappable
4. ✅ Close button accessible
5. ✅ No layout broken elements

---

### Scenario 7: Permission & Security

**Goal:** Verify users can only modify their own posts

**Setup:** 2 user accounts (User A, User B)

**Test 7a: Image Upload Permission**
1. User A creates post (ID: 123)
2. User B attempts POST `/api/posts/123/upload_images/`
3. ✅ Should return 403 Forbidden: "Permission denied"
4. Images not uploaded
5. Database unchanged

**Test 7b: Image Delete Permission**
1. User A creates post with 3 images
2. User B attempts DELETE `/api/posts/123/delete_image/999/`
3. ✅ Should return 403 Forbidden
4. Image still in database
5. Gallery still shows 3 images for User A

**Test 7c: Own Post Can Modify**
1. User A creates post with 3 images
2. User A deletes 1 image via API
3. ✅ POST `delete_image` succeeds (204)
4. Gallery now shows 2 images
5. Database updated correctly

---

### Scenario 8: Error Recovery

**Goal:** Verify graceful error handling

**Test 8a: Network Failure During Upload**
1. Create post with 5 images
2. Start upload
3. Interrupt network (DevTools → Offline)
4. ✅ Should show error message
5. ✅ Form stays on page (no redirect)
6. ✅ Can retry upload
7. Restore network, retry succeeds

**Test 8b: Invalid Post ID**
1. Manually POST to `/api/posts/9999/upload_images/` (fake ID)
2. ✅ Should return 404 Not Found
3. Frontend shows error message

**Test 8c: Partially Uploaded**
1. Create post with 10 images
2. Upload starts
3. 7 images upload successfully, then network fails
4. ✅ 7 images saved in database
5. Can retry remaining images, or delete and recreate

---

### Scenario 9: Backward Compatibility

**Goal:** Verify old posts without images still work

**Setup:** Have old posts in database with `image_url` but no `images` array

**Test:**
1. View dashboard/feed
2. ✅ Old posts still display (single image from `image_url`)
3. ✅ No errors in console
4. ✅ Can view old post details
5. ✅ Gallery gracefully falls back to legacy image

---

### Scenario 10: Database State

**Goal:** Verify database integrity

**Test:**
```sql
-- Count posts with images
SELECT COUNT(DISTINCT post_id) FROM posts_postimage;
-- Should match number of multi-image posts created

-- Verify relationships
SELECT p.id, COUNT(pi.id) as image_count
FROM posts_post p
LEFT JOIN posts_postimage pi ON p.id = pi.post_id
GROUP BY p.id;
-- Should show 0-15 images per post

-- Check cascade delete
DELETE FROM posts_post WHERE id=1;
SELECT COUNT(*) FROM posts_postimage WHERE post_id=1;
-- Should be 0 (cascade deleted)
```

---

## 📊 Test Results Template

### Test Run #1: [Date/Time]

| Test | Status | Notes | Duration |
|------|--------|-------|----------|
| 1.0 Basic Upload | ✅ PASS | All 3 images uploaded | 2m |
| 2.1 Exactly 15 | ✅ PASS | Uploaded all 15 | 3m |
| 2.2 16 Images | ✅ PASS | Rejected with error | 1m |
| 3.1 5MB Image | ✅ PASS | Accepted | 1m |
| 3.2 5.1MB Image | ✅ PASS | Rejected with error | 1m |
| 4.1 Valid Formats | ✅ PASS | JPEG, PNG, GIF, WebP all work | 5m |
| 4.2 Invalid Formats | ✅ PASS | PDF, DOCX rejected | 3m |
| 5.1 Thumbnail Strip | ✅ PASS | All thumbnails visible | 2m |
| 5.2 Click Switch | ✅ PASS | Image switches on click | 1m |
| 5.3 Modal Open | ✅ PASS | Modal displays | 1m |
| 5.4 Arrow Navigation | ✅ PASS | Next/Prev works | 2m |
| 5.5 Close Modal | ✅ PASS | × button works | 1m |
| 6.1 Form Mobile | ✅ PASS | Responsive on iPhone | 5m |
| 6.2 Gallery Mobile | ✅ PASS | Thumbnails scroll | 3m |
| 6.3 Modal Mobile | ✅ PASS | Full-screen works | 2m |
| 7.1 Permission Upload | ✅ PASS | 403 on other user | 2m |
| 7.2 Permission Delete | ✅ PASS | 403 on other user | 1m |
| 7.3 Own Post Modify | ✅ PASS | Can delete own images | 2m |
| 8.1 Network Error | ✅ PASS | Graceful error message | 2m |
| 8.2 Invalid ID | ✅ PASS | 404 shown | 1m |
| 8.3 Partial Upload | ✅ PASS | Partial images saved | 2m |
| 9.0 Backward Compat | ✅ PASS | Old posts work | 2m |
| 10.0 Database | ✅ PASS | Relationships intact | 1m |

**Summary:** 22/22 PASS | **Duration:** 50 minutes | **Issues Found:** 0

---

## 🐛 Bug Report Template

If you find an issue:

```
## Bug: [Title]

### Steps to Reproduce
1. ...
2. ...
3. ...

### Expected Result
...

### Actual Result
...

### Environment
- Browser: Chrome/Safari/Firefox
- Device: Desktop/Mobile
- OS: Windows/Mac/Linux/iOS/Android
- URL: http://...

### Console Errors
[Paste any JavaScript errors from DevTools]

### API Response
[Paste response from Network tab]

### Screenshots/Video
[Attach if helpful]

### Severity
[ ] Critical (feature completely broken)
[ ] Major (feature partially broken)
[ ] Minor (cosmetic issue)
```

---

## ✅ Sign-Off Checklist

Before releasing feature:

- [ ] All 22 tests passed
- [ ] No console errors on Chrome/Firefox/Safari
- [ ] Mobile tested on real device (not just emulator)
- [ ] Permissions verified (can't delete other users' images)
- [ ] Database cascade delete verified
- [ ] Backward compatibility confirmed
- [ ] Performance acceptable (<2s upload for 5 images)
- [ ] Documentation complete and accurate

---

**Last Updated:** January 10, 2026 | **Maintained by:** QA Team
