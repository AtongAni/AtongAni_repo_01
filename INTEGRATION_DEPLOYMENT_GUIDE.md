# Integration & Deployment Guide

## Step 1: Backend Deployment

### 1.1 Install Dependencies
```bash
cd farmers-market
pip install django djangorestframework djangorestframework-simplejwt
```

### 1.2 Register Orders App
✅ **Already Done** - 'orders' added to INSTALLED_APPS in `config/settings.py`

Verify in `config/settings.py` line 46:
```python
INSTALLED_APPS = [
    ...
    'orders',  # ✅ This line should be present
]
```

### 1.3 Include Order URLs
✅ **Already Done** - Orders URLs included in `config/urls.py`

Verify in `config/urls.py` line 26:
```python
urlpatterns = [
    ...
    path("api/", include("orders.urls")),  # ✅ This line should be present
]
```

### 1.4 Run Database Migrations
```bash
python manage.py migrate
```

**Expected output:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, messages, staticfiles, 
                       rest_framework, accounts, posts, comments, cart, orders
Running migrations:
  Applying orders.0001_initial... OK
```

### 1.5 Create Test Users (Optional)
```bash
python manage.py shell
```

In Python shell:
```python
from accounts.models import User, FarmerProfile
from posts.models import Post

# Create farmer
farmer = User.objects.create_user(
    username='farmer_test',
    password='test123',
    role='FARMER'
)
FarmerProfile.objects.create(user=farmer, farm_name='Test Farm')

# Create customer
customer = User.objects.create_user(
    username='customer_test',
    password='test123',
    role='CUSTOMER'
)

# Create product
Post.objects.create(
    author=farmer,
    title='Tomatoes',
    content='Fresh tomatoes',
    price=50,
    quantity=100,
    unit='KG'
)

exit()
```

### 1.6 Start Backend Server
```bash
python manage.py runserver
```

**Should see:**
```
Django version 6.0, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
```

## Step 2: Frontend Integration

### 2.1 Verify Component Files Exist
Check these files are present:
```
✅ web/src/api/orders.js
✅ web/src/components/OrdersView.jsx
✅ web/src/components/OrdersView.css
✅ web/src/components/FarmerOrdersManagement.jsx
✅ web/src/components/FarmerOrdersManagement.css
✅ web/src/components/CartView.jsx (Updated)
✅ web/src/components/CartView.css (Updated)
```

### 2.2 Import Components in Your Main App

Edit your main routing/layout file (e.g., `Dashboard.jsx` or `App.jsx`):

```jsx
// At the top of your file, add imports:
import OrdersView from './components/OrdersView';
import FarmerOrdersManagement from './components/FarmerOrdersManagement';

// In your JSX, add the components:

// For Customer Dashboard:
function CustomerDashboard() {
  return (
    <div>
      <CartView />
      <OrdersView />  {/* Add this line */}
    </div>
  );
}

// For Farmer Dashboard:
function FarmerDashboard() {
  return (
    <div>
      <FarmerOrdersManagement />  {/* Add this line */}
      {/* ... other farmer components ... */}
    </div>
  );
}
```

### 2.3 Install Frontend Dependencies (if needed)
```bash
cd web
npm install
```

### 2.4 Start Frontend Development Server
```bash
npm run dev
```

**Should see:**
```
  VITE v... dev server running at:

  ➜  Local:   http://localhost:5173/
```

## Step 3: Test the Complete Flow

### 3.1 Test Customer Checkout

1. **Open browser**: `http://localhost:5173`
2. **Login as customer**:
   - Username: `customer_test`
   - Password: `test123`
3. **Add item to cart**:
   - Find product "Tomatoes"
   - Add 10 KG to cart
4. **Go to cart**
5. **Click "Proceed to Checkout"**
   - Should see: Order confirmation with "In Progress" status
   - Should see: Order #X with items listed
   - Should see: "⏳ Your order is awaiting farmer approval..."

### 3.2 Test Farmer Approval

1. **Open new browser tab/window**
2. **Login as farmer**:
   - Username: `farmer_test`
   - Password: `test123`
3. **Go to Order Management**
   - Should see: Order #X from customer_test
   - Should see: Items (10 KG Tomatoes)
   - Should see: Accept and Reject buttons
4. **Click "Accept Order"**
   - Should see: Success message
   - Order disappears from pending list
5. **Verify in Django Admin**:
   - Go to `http://localhost:8000/admin`
   - Check Orders: Status should be "APPROVED"
   - Check Products: Tomatoes quantity should be 90 KG (100-10)

### 3.3 Test Order View (Customer)

1. **Switch back to customer tab**
2. **Click "My Orders"** (or OrdersView component)
   - Should see: Order #X with "✅ APPROVED" status
   - Status should change within 5 seconds if order just approved

### 3.4 Test Rejection Flow

1. **As customer**: Create new order
2. **As farmer**: Click "Reject Order"
   - Enter reason: "Out of stock"
   - Click "Confirm Rejection"
3. **Verify**:
   - Order status shows "❌ REJECTED"
   - Rejection reason displayed
   - Inventory unchanged
   - Items back in customer's cart

## Step 4: API Testing (Optional)

### 4.1 Get Authentication Token
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "customer_test",
    "password": "test123"
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 4.2 Test Order Creation
```bash
curl -X POST http://localhost:8000/api/orders/checkout/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

### 4.3 Test Get Orders
```bash
curl -X GET http://localhost:8000/api/orders/my_orders/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4.4 Test Get Pending Orders (Farmer)
```bash
curl -X GET http://localhost:8000/api/orders/my_pending_orders/ \
  -H "Authorization: Bearer YOUR_FARMER_TOKEN"
```

## Step 5: Production Deployment

### 5.1 Environment Setup
Create `.env` file:
```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### 5.2 Database Migration
```bash
# For PostgreSQL (recommended for production)
python manage.py migrate --database=postgresql
```

### 5.3 Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 5.4 Build Frontend
```bash
cd web
npm run build
```

### 5.5 Deploy with Gunicorn/uWSGI
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Verification Checklist

### Backend
- [ ] Orders app appears in Django admin
- [ ] Order and OrderItem models visible in admin
- [ ] Migrations run successfully
- [ ] API endpoints respond correctly
- [ ] Authentication works
- [ ] CORS enabled for frontend requests

### Frontend
- [ ] CartView shows checkout button
- [ ] OrdersView displays orders correctly
- [ ] FarmerOrdersManagement shows pending orders
- [ ] Polling updates work (watch network tab)
- [ ] Buttons are clickable and functional
- [ ] Messages display on success/error

### Integration
- [ ] Customer can create order
- [ ] Order appears in farmer's pending list
- [ ] Farmer can approve order
- [ ] Inventory reduces after approval
- [ ] Order status updates in customer view
- [ ] Rejection returns items to cart
- [ ] No errors in browser console
- [ ] No errors in Django logs

## Troubleshooting Deployment

### Issue: 500 Error on Checkout
**Solution:**
1. Check Django logs: `python manage.py runserver` output
2. Verify orders app is in INSTALLED_APPS
3. Run migrations: `python manage.py migrate`
4. Check database connection

### Issue: Orders not showing in pending list
**Solution:**
1. Verify farmer has FarmerProfile
2. Verify product belongs to farmer
3. Check order status is IN_PROGRESS
4. Check API response in browser dev tools

### Issue: CORS Errors
**Solution:**
1. Verify CORS_ALLOW_ALL_ORIGINS = True in settings
2. Or add frontend URL to CORS_ALLOWED_ORIGINS
3. Check OPTIONS request is successful

### Issue: Inventory not reducing
**Solution:**
1. Check post.quantity is DecimalField
2. Check order approval is being called
3. Verify transaction is being committed
4. Check Django logs for database errors

## Documentation Files

Refer to these files for more information:
- `IMPLEMENTATION_COMPLETE.md` - Complete implementation overview
- `CHECKOUT_STAGING_IMPLEMENTATION.md` - Technical documentation
- `CHECKOUT_STAGING_QUICKSTART.md` - Quick testing guide

## Support Resources

- Django Docs: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- React Docs: https://react.dev/
- JWT Authentication: https://github.com/jpadilla/django-rest-framework-simplejwt

## Next Steps

1. ✅ Follow all steps above
2. ✅ Test the complete flow
3. ✅ Customize styling as needed
4. ✅ Add email notifications (future enhancement)
5. ✅ Deploy to production

**You're all set!** The checkout staging system is ready to use. 🎉
