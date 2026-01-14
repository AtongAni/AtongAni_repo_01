# Developer's Quick Reference

## 🚀 Quick Start Commands

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run linting
npm run lint
```

## 📍 Key Locations

| What | Where |
|------|-------|
| Main App | `src/App.jsx` |
| Dashboard | `src/pages/Dashboard.jsx` |
| Components | `src/components/` |
| API Calls | `src/api/` |
| Styles | `*.css` files in each folder |

## 🧩 Components at a Glance

| Component | Purpose | Location |
|-----------|---------|----------|
| Dashboard | Main container with tabs | `src/pages/Dashboard.jsx` |
| PostFeed | Display posts with filters | `src/components/PostFeed.jsx` |
| PostCard | Individual post | `src/components/PostCard.jsx` |
| CommentsSection | Comments UI | `src/components/CommentsSection.jsx` |
| FarmerPostForm | Create posts | `src/components/FarmerPostForm.jsx` |
| CartView | Shopping cart | `src/components/CartView.jsx` |

## 🔗 API Quick Reference

### Posts
```javascript
import { getPosts, createPost } from '../api/posts';

// Get posts
const { data } = await getPosts({ role: 'farmer' }); // optional filter

// Create post
await createPost({ title, content, price });
```

### Comments
```javascript
import { getComments, createComment, deleteComment } from '../api/comments';

// Get comments
await getComments(postId);

// Create comment
await createComment(postId, { text });

// Delete comment
await deleteComment(postId, commentId);
```

### Cart
```javascript
import { getCart, addToCart, checkoutCart } from '../api/cart';

// Get cart
const { data } = await getCart();

// Add to cart
await addToCart(postId, quantity);

// Checkout
await checkoutCart();
```

## 🎯 Common Tasks

### Add a New Feature to PostCard
1. Edit `src/components/PostCard.jsx`
2. Update `src/components/PostCard.css`
3. Import any new API functions
4. Add state with `useState`
5. Handle errors with try-catch

### Change Colors
Edit the gradient in `src/pages/Dashboard.css`:
```css
background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
```

### Add a New Tab
1. Add case in `activeTab` state in `Dashboard.jsx`
2. Add button in tabs navigation
3. Add content section in main area
4. Style with `tab-content` class

### Fix Mobile Layout
1. Check responsive breakpoints in CSS (480px, 768px)
2. Test in browser DevTools mobile view
3. Adjust padding/margins
4. Ensure buttons are 44px min height

## 🔐 Authentication Flow

```javascript
// Login
const token = await login({ username, password });
localStorage.setItem('access', token);

// Use token
setAuthToken(token); // Sets Bearer header

// Logout
localStorage.removeItem('access');
setAuthToken(null);
```

## 💾 Local Storage

```javascript
// Store token
localStorage.setItem('access', token);

// Get token
const token = localStorage.getItem('access');

// Remove token
localStorage.removeItem('access');
```

## 📱 Responsive Breakpoints

```css
/* Mobile (default) */
/* Styles apply to screens < 480px */

/* Tablet */
@media (max-width: 768px) { }

/* Mobile specific */
@media (max-width: 480px) { }
```

## 🎨 Color Variables

```javascript
// Primary Colors
const PRIMARY = '#667eea';      // Purple
const SECONDARY = '#764ba2';    // Dark purple

// Status Colors
const SUCCESS = '#4caf50';      // Green
const DANGER = '#d32f2f';       // Red
const WARNING = '#ff9800';      // Orange

// Neutral Colors
const LIGHT = '#f5f5f5';        // Light gray
const MEDIUM = '#e0e0e0';       // Medium gray
const DARK = '#333333';         // Dark gray
```

## 🔄 State Management Pattern

```javascript
// 1. Define state
const [data, setData] = useState(null);
const [loading, setLoading] = useState(false);
const [error, setError] = useState('');

// 2. Load data
useEffect(() => {
  loadData();
}, [dependencies]);

// 3. Handle errors
async function loadData() {
  setLoading(true);
  try {
    const res = await apiCall();
    setData(res.data);
  } catch (err) {
    setError('Error message');
  } finally {
    setLoading(false);
  }
}

// 4. Render states
if (loading) return <div>Loading...</div>;
if (error) return <div>{error}</div>;
return <div>{/* Render data */}</div>;
```

## 🧪 Console Debugging

```javascript
// Log API responses
console.log('Response:', res.data);

// Check user state
console.log('User:', user);

// Check component props
console.log('Props:', props);

// Check errors
console.error('Error:', err);
```

## 🎯 Form Validation Pattern

```javascript
// 1. Validation function
function validate() {
  if (!title.trim()) return 'Title required';
  if (title.length > 100) return 'Title too long';
  return null;
}

// 2. Use in submit
async function handleSubmit(e) {
  e.preventDefault();
  const error = validate();
  if (error) {
    setError(error);
    return;
  }
  // Submit...
}
```

## 🔌 Adding New API Endpoint

1. Create function in `src/api/[module].js`:
```javascript
export function myNewFunction(data) {
  return api.post('/api/endpoint/', data);
}
```

2. Import in component:
```javascript
import { myNewFunction } from '../api/module';
```

3. Use in component:
```javascript
const res = await myNewFunction(data);
```

## 📊 Data Flow Example

```
User Action (Click button)
    ↓
Event Handler (onClick)
    ↓
State Update (setState)
    ↓
API Call (async/await)
    ↓
Backend Response
    ↓
Update UI (re-render)
    ↓
Show to User
```

## ⚠️ Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forgetting `await` on async | Add `await` before async calls |
| Wrong import path | Use relative paths like `../api/` |
| State not updating | Check async/await flow |
| CSS not applying | Check class name spelling |
| Token not sending | Ensure `setAuthToken()` called |
| Mobile layout broken | Check media query breakpoints |

## 🔍 Quick Debugging Checklist

- [ ] Check browser console for errors
- [ ] Check network tab for API responses
- [ ] Verify localStorage has token
- [ ] Check component props passed correctly
- [ ] Verify CSS classes match
- [ ] Check API endpoint URL
- [ ] Verify async/await usage
- [ ] Check useState initialization
- [ ] Check useEffect dependencies

## 📚 File Templates

### New Component Template
```javascript
import { useState } from "react";
import "./ComponentName.css";

export default function ComponentName({ prop }) {
  const [state, setState] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function handleAction() {
    // Implementation
  }

  if (loading) return <div>Loading...</div>;

  return (
    <div className="component-name">
      {error && <div className="error">{error}</div>}
      {/* JSX */}
    </div>
  );
}
```

### New API Module Template
```javascript
import { api } from "./client";

export function getResource() {
  return api.get("/api/resource/");
}

export function createResource(data) {
  return api.post("/api/resource/", data);
}

export function updateResource(id, data) {
  return api.patch(`/api/resource/${id}/`, data);
}

export function deleteResource(id) {
  return api.delete(`/api/resource/${id}/`);
}
```

## 🚀 Performance Tips

1. **Memoize components**: Use `React.memo()` for expensive components
2. **Lazy load**: Use `React.lazy()` for code splitting
3. **Optimize re-renders**: Check useEffect dependencies
4. **Debounce searches**: Add delay for search inputs
5. **Cache API responses**: Store frequently accessed data

## 🔐 Security Tips

1. Never store sensitive data in localStorage
2. Always validate user input
3. Use HTTPS in production
4. Set secure CORS headers
5. Sanitize user-generated content
6. Use environment variables for API URLs
7. Never commit `.env` with real values

## 📖 Where to Learn More

- FEATURES.md - Complete feature documentation
- QUICKSTART.md - Getting started guide
- BACKEND_INTEGRATION.md - Backend setup
- COMPONENT_ARCHITECTURE.md - Code structure
- IMPLEMENTATION_SUMMARY.md - Changes overview

---

**Happy coding!** 🎉

*For detailed info, see the documentation files in the web folder.*
