# Farmers Market Dashboard - Features Documentation

## 📋 Overview
This enhanced dashboard provides a complete marketplace experience with distinct features for customers and farmers. The application is fully responsive and optimized for mobile devices.

## ✨ Key Features

### 1. **Post Feed** (Available to All Users)
- Browse posts from all users or filter by farmers only
- View product details including title, description, price, and author info
- Real-time timestamp display
- Mobile-friendly card layout

**Location:** `src/components/PostFeed.jsx`

### 2. **Comments System** (Available to All Users)
- Comment on any post with a character limit (500 chars)
- View all comments on a post
- Delete your own comments
- Author and timestamp display for each comment
- Real-time comment updates

**Location:** `src/components/CommentsSection.jsx`

### 3. **Shopping Cart** (Customers Only)
- Add items from farmer posts to your cart
- Adjust quantities with + and - buttons
- Remove items from cart
- View cart subtotal and total
- Proceed to checkout
- Empty cart state with helpful message

**Features:**
- Persists cart data via backend API
- Shows farmer names and product details
- Item quantity adjustment
- Real-time total calculation

**Location:** `src/components/CartView.jsx`

### 4. **Farmer Post Creation** (Farmers Only)
- Create new posts with title, description, and optional price
- Character limits for data validation (Title: 100, Description: 1000)
- Form validation with user-friendly error messages
- Success feedback after post creation
- Auto-populated character counters

**Location:** `src/components/FarmerPostForm.jsx`

### 5. **User Profile** (Available to All Users)
- View account information (username, email, account type)
- See member since date
- One-click logout
- Clean, organized profile card

**Accessible via:** Profile tab in the dashboard

### 6. **Role-Based Navigation**
The dashboard adapts based on user role:

**Farmers see:**
- Feed tab (browse all posts)
- My Posts tab (create and manage posts)
- Profile tab

**Customers see:**
- Feed tab (browse all posts)
- Cart tab (manage shopping cart)
- Profile tab

## 🎨 UI/UX Highlights

### Mobile-Friendly Design
- Responsive breakpoints at 480px, 768px
- Touch-friendly buttons and inputs
- Optimized spacing and padding for small screens
- Horizontal scrolling for tabs on mobile
- Readable text sizes on all devices

### Color Scheme
- **Primary:** #667eea (purple)
- **Secondary:** #764ba2 (dark purple)
- **Success:** #4caf50 (green)
- **Danger:** #d32f2f (red)
- **Neutral:** #f5f5f5 (light gray)

### Components
- **Gradient Header:** Distinctive header with user info
- **Tab Navigation:** Easy switching between sections
- **Cards:** Consistent card design for posts and items
- **Buttons:** Clear action buttons with hover states
- **Forms:** Validated input fields with character counters
- **Status Messages:** Color-coded feedback (success/error)

## 📁 File Structure

```
src/
├── api/
│   ├── auth.js           (Authentication endpoints)
│   ├── posts.js          (Post CRUD operations)
│   ├── comments.js       (Comment operations)
│   ├── cart.js           (Cart management)
│   └── client.js         (Axios configuration)
├── components/
│   ├── PostFeed.jsx      (Feed display with filters)
│   ├── PostCard.jsx      (Individual post card)
│   ├── CommentsSection.jsx (Comments for a post)
│   ├── FarmerPostForm.jsx (Post creation form)
│   ├── CartView.jsx      (Shopping cart view)
│   └── *.css             (Component styles)
├── pages/
│   ├── Dashboard.jsx     (Main dashboard with tabs)
│   ├── Dashboard.css     (Dashboard styles)
│   ├── Login.jsx         (Login/Register)
│   └── Welcome.jsx       (Landing page)
└── main.jsx
```

## 🔌 API Endpoints (Expected Backend)

### Posts
- `GET /api/posts/` - List all posts (supports filtering)
- `POST /api/posts/` - Create new post
- `GET /api/posts/{id}/` - Get post details
- `PATCH /api/posts/{id}/` - Update post
- `DELETE /api/posts/{id}/` - Delete post

### Comments
- `GET /api/posts/{postId}/comments/` - List comments
- `POST /api/posts/{postId}/comments/` - Create comment
- `PATCH /api/posts/{postId}/comments/{commentId}/` - Update comment
- `DELETE /api/posts/{postId}/comments/{commentId}/` - Delete comment

### Cart
- `GET /api/cart/` - Get user's cart
- `POST /api/cart/` - Add item to cart
- `PATCH /api/cart/{id}/` - Update cart item quantity
- `DELETE /api/cart/{id}/` - Remove item from cart
- `POST /api/cart/checkout/` - Process checkout

## 🚀 Usage Guide

### For Customers
1. Login with customer account
2. Browse "Feed" tab to see all posts
3. Click on post to see comments and details
4. Click "Add to Cart" to purchase items
5. Go to "Cart" tab to review and checkout
6. Manage profile in "Profile" tab

### For Farmers
1. Login with farmer account
2. Go to "My Posts" tab
3. Fill out the form and click "Post"
4. Your post appears in the feed
5. Customers can comment on your posts
6. Browse "Feed" to see other posts and comments

## 💡 Implementation Notes

### State Management
- Uses React hooks (useState, useEffect)
- Local storage for authentication token
- Refresh triggers for real-time updates

### Error Handling
- User-friendly error messages
- Loading states during API calls
- Graceful fallbacks for failed requests

### Validation
- Character limits with counter display
- Required field validation
- Email format validation
- Password confirmation matching

### Performance
- Component-level code splitting
- Lazy loading of components
- Efficient re-renders using dependency arrays
- Optimized CSS with minimal specificity

## 🔐 Security Considerations
- JWT token stored in localStorage
- Bearer token sent with API requests
- Protected routes requiring authentication
- Input validation and sanitization
- CORS handled by backend

## 📱 Browser Support
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🐛 Known Limitations
- Cart persists only in session
- No image upload for posts (use external URLs)
- No pagination for large post lists
- No search functionality (basic filtering only)

## 🔄 Future Enhancements
- Post search functionality
- Advanced filtering (by price, date, rating)
- Post ratings/reviews system
- User profile pictures
- Order history
- Notifications system
- Direct messaging between users
- Post image uploads
- Pagination/infinite scroll
- Post editing capabilities
