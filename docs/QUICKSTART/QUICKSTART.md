# Quick Start Guide - Farmers Market Dashboard

## 🎯 What's New

Your dashboard now includes:
- **Posts Feed** - Browse all farmer posts
- **Comments** - Comment on posts and interact with community
- **Shopping Cart** - Add items to cart and checkout (customers only)
- **Post Creation** - Create and manage posts (farmers only)
- **User Profiles** - View account information

## 📁 New Files Created

### API Modules
- `src/api/posts.js` - Post API calls
- `src/api/comments.js` - Comment API calls
- `src/api/cart.js` - Cart API calls

### Components
- `src/components/PostFeed.jsx` - Main feed display
- `src/components/PostCard.jsx` - Individual post card
- `src/components/CommentsSection.jsx` - Comments UI
- `src/components/FarmerPostForm.jsx` - Post creation form
- `src/components/CartView.jsx` - Shopping cart

### Stylesheets
- `src/components/*.css` - Component styles (mobile-friendly)
- `src/pages/Dashboard.css` - Dashboard layout styles

### Documentation
- `FEATURES.md` - Complete feature documentation
- `BACKEND_INTEGRATION.md` - Backend setup guide

## 🚀 Running the Project

```bash
# Install dependencies (if not already done)
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## 🔗 Key Routes

- `/` - Welcome page
- `/login` - Login/Register
- `/dashboard` - Main dashboard (protected)

## 👥 User Roles

### Customer
- Create account with "Customer" role
- Browse posts in Feed
- Add items to cart
- Comment on posts
- View cart and checkout

### Farmer
- Create account with "Farmer" role
- Create new posts
- Comment on other posts
- Browse all posts

## 🎨 Dashboard Tabs

The dashboard has different tabs based on your role:

**All Users:**
- 📰 Feed - Browse all posts
- ⚙️ Profile - Account settings

**Farmers Only:**
- 📝 My Posts - Create and manage posts

**Customers Only:**
- 🛒 Cart - Shopping cart

## 💻 Development Notes

### Component Structure
All components use React hooks and functional components. No class components.

### Styling
- Mobile-first responsive design
- CSS modules imported separately
- Color scheme defined in component files
- Responsive breakpoints at 480px and 768px

### State Management
- Local component state with useState
- Effects for data loading with useEffect
- Token stored in localStorage
- API calls with axios (configured in client.js)

### Error Handling
- Try-catch blocks for async operations
- User-friendly error messages
- Loading states while fetching data
- Validation on form submission

## 🔧 Customization

### Change Colors
Edit the gradient in `src/pages/Dashboard.css`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Adjust Breakpoints
Modify media queries in `*.css` files:
```css
@media (max-width: 480px) { /* Mobile */ }
@media (max-width: 768px) { /* Tablet */ }
```

### Modify API Base URL
Edit `src/api/client.js`:
```javascript
const baseURL = import.meta.env.VITE_API_URL || "/";
```

Set `VITE_API_URL` in `.env`:
```
VITE_API_URL=https://your-api-url.com
```

## 📝 Form Validation

### Post Creation
- Title: required, max 100 chars
- Description: required, max 1000 chars
- Price: optional number

### Comments
- Text: required, max 500 chars

### Cart
- Quantities: 1 or more

## 🔒 Authentication Flow

1. User registers/logs in
2. Backend returns JWT token
3. Token stored in localStorage
4. Token sent with all API requests
5. On logout, token removed from localStorage

## 🐛 Troubleshooting

### "Loading..." stuck indefinitely
- Check if backend is running
- Verify API URL in `.env`
- Check browser console for errors

### Posts not showing
- Verify backend has `GET /api/posts/` endpoint
- Check that posts exist in backend
- Look for API errors in browser network tab

### Can't add to cart
- Ensure you're logged in as customer
- Check if post has a price
- Verify `POST /api/cart/` endpoint exists

### Comments not posting
- Check character limit (500 max)
- Verify authentication token is valid
- Look for API errors in console

## 📦 Dependencies

Core packages:
- `react` - UI framework
- `react-router-dom` - Routing
- `axios` - HTTP client
- `vite` - Build tool

See `package.json` for full list.

## 📞 Support

For issues or questions:
1. Check the FEATURES.md for detailed documentation
2. Review BACKEND_INTEGRATION.md for backend setup
3. Check browser console for JavaScript errors
4. Check network tab for API responses

## ✅ Testing Checklist

- [ ] Can login with customer account
- [ ] Can login with farmer account
- [ ] Can view posts in feed
- [ ] Can add comment to post
- [ ] Can delete own comment
- [ ] Can add item to cart (customer only)
- [ ] Can adjust cart quantities
- [ ] Can checkout cart
- [ ] Can create post (farmer only)
- [ ] Can view profile
- [ ] Can logout
- [ ] Layout is responsive on mobile

---

Happy coding! 🎉
