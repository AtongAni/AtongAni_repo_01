# Component Architecture Guide

## 📐 Component Hierarchy

```
App.jsx (Router)
├── Login.jsx (Authentication)
├── Welcome.jsx (Landing)
└── Dashboard.jsx (Main App - Protected Route)
    ├── Header
    │   ├── Title
    │   └── User Info
    ├── Navigation Tabs
    │   ├── Feed Tab
    │   ├── My Posts Tab (Farmers)
    │   ├── Cart Tab (Customers)
    │   └── Profile Tab
    └── Content Area
        ├── PostFeed Component
        │   ├── Filter Buttons
        │   └── Posts List
        │       └── PostCard Component (repeated)
        │           ├── Post Header (Author + Price)
        │           ├── Post Content
        │           ├── Post Image
        │           └── Actions
        │               ├── Comment Button
        │               ├── Add to Cart Button
        │               └── CommentsSection Component
        │                   ├── Comment Form
        │                   └── Comments List
        ├── FarmerPostForm Component (Farmers)
        │   ├── Form Fields
        │   └── Submit Button
        ├── CartView Component (Customers)
        │   ├── Cart Items List
        │   │   └── CartItem (repeated)
        │   ├── Cart Summary
        │   └── Checkout Button
        └── Profile View
            └── Profile Card
```

## 🔄 Data Flow

### Posts Display Flow
```
Dashboard (activeTab="feed")
  ↓
PostFeed.jsx (fetches posts)
  ↓
getPosts() [api/posts.js]
  ↓
Backend: GET /api/posts/
  ↓
PostCard.jsx (rendered for each post)
  ↓
Post data displayed with author, price, comments
```

### Comment Flow
```
PostCard.jsx (user clicks comment)
  ↓
CommentsSection.jsx (toggles visibility)
  ↓
getComments() [api/comments.js]
  ↓
Backend: GET /api/posts/{id}/comments/
  ↓
Comment form shown
  ↓
User submits → createComment()
  ↓
Backend: POST /api/posts/{id}/comments/
  ↓
Comments list refreshed
```

### Cart Flow
```
PostCard.jsx (user clicks "Add to Cart")
  ↓
handleAddToCart()
  ↓
addToCart() [api/cart.js]
  ↓
Backend: POST /api/cart/
  ↓
Success message shown
  ↓
User navigates to Cart tab
  ↓
CartView.jsx (fetches cart)
  ↓
getCart() [api/cart.js]
  ↓
Backend: GET /api/cart/
  ↓
Cart items displayed with quantities
```

## 🧩 Component Details

### Dashboard.jsx
**Purpose:** Main container and tab manager
**State:**
- `user` - Current logged-in user
- `activeTab` - Current active tab
- `refreshFeed` - Trigger for feed refresh
**Props:** None (uses auth from localStorage)
**Children:** All tab components

### PostFeed.jsx
**Purpose:** Display and filter posts
**State:**
- `posts` - Array of posts
- `loading` - Loading state
- `error` - Error message
- `filter` - Current filter ("all" or "farmers")
**Props:**
- `user` - Current user object
- `refreshTrigger` - Trigger refresh
**Children:** PostCard components

### PostCard.jsx
**Purpose:** Individual post display with actions
**State:**
- `showComments` - Toggle comments visibility
- `cartLoading` - Add to cart loading state
- `cartError` - Cart error message
**Props:**
- `post` - Post object
- `user` - Current user
- `onRefresh` - Callback to refresh
**Children:** CommentsSection

### CommentsSection.jsx
**Purpose:** Display and manage comments for a post
**State:**
- `comments` - Array of comments
- `newComment` - Comment form input
- `loading` - Submit loading state
- `error` - Error message
**Props:**
- `postId` - ID of the post
- `user` - Current user
- `onRefresh` - Callback to refresh
**Children:** None

### FarmerPostForm.jsx
**Purpose:** Post creation form for farmers
**State:**
- `title` - Post title
- `content` - Post description
- `price` - Product price
- `loading` - Submit loading state
- `error` - Error message
- `success` - Success message
**Props:**
- `onPostCreated` - Callback when post created
**Children:** None

### CartView.jsx
**Purpose:** Shopping cart display and management
**State:**
- `cartItems` - Array of cart items
- `loading` - Loading state
- `error` - Error message
- `checkingOut` - Checkout loading state
**Props:** None
**Children:** None

## 🔐 Protected Routes

```javascript
// App.jsx
<ProtectedRoute>
  <Dashboard />
</ProtectedRoute>
```

The ProtectedRoute checks for valid token before rendering Dashboard.

## 🎣 Custom Hooks (Future Enhancement)

You could extract common logic into custom hooks:

```javascript
// Example: useAuth hook
const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Auth logic
  }, []);
  
  return { user, loading };
};

// Usage
const { user, loading } = useAuth();
```

## 📊 State Management Strategy

Currently using local component state. For scaling, consider:

1. **Context API** (simple)
   ```javascript
   const UserContext = createContext();
   
   <UserContext.Provider value={user}>
     <Dashboard />
   </UserContext.Provider>
   ```

2. **Redux** (complex apps)
   - For large state trees
   - Complex state updates
   - Many components sharing state

3. **Zustand** (lightweight)
   - Similar to Redux but simpler
   - Good for medium-sized apps

## 🔗 API Integration Points

Each component integrates with API through separate files:

| Component | API File | Endpoints |
|-----------|----------|-----------|
| PostFeed | posts.js | GET /posts |
| PostCard | cart.js | POST /cart |
| CommentsSection | comments.js | GET, POST, DELETE /comments |
| FarmerPostForm | posts.js | POST /posts |
| CartView | cart.js | GET, PATCH, DELETE, POST /cart |

## ⚡ Performance Optimizations

1. **Memoization** (React.memo for PostCard)
   ```javascript
   export default React.memo(PostCard);
   ```

2. **Lazy Loading** (for components)
   ```javascript
   const CartView = React.lazy(() => import('./CartView'));
   ```

3. **Dependency Arrays** (useEffect optimization)
   ```javascript
   useEffect(() => { }, [postId, refreshTrigger]);
   ```

## 🎨 Styling Architecture

Each component has its own CSS file:
- `Component.jsx` - Logic
- `Component.css` - Styles

**Naming Convention:**
- `.component-name` - Main container
- `.component-name-[part]` - Sub-elements
- `.is-[state]` - State classes (is-active)
- `.has-[modifier]` - Modifier classes

**Example:**
```css
.post-card { } /* Main */
.post-header { } /* Sub-element */
.post-card.has-error { } /* Modifier */
```

## 🧪 Testing Strategy

Components can be tested with React Testing Library:

```javascript
// Example test
test('PostCard displays post title', () => {
  render(<PostCard post={mockPost} user={mockUser} />);
  expect(screen.getByText(mockPost.title)).toBeInTheDocument();
});
```

## 📚 Component Reusability

These components could be reused:
- `PostCard` - Could be used in other layouts
- `CommentsSection` - Generic comments system
- `CartView` - Could be a modal or page
- `FarmerPostForm` - Could support editing

Just adjust props as needed!

---

For more details, see FEATURES.md and BACKEND_INTEGRATION.md
