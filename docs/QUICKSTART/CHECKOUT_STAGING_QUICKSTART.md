# Checkout Staging System - Quick Start Guide

## Setup Instructions

### Backend Setup

1. **Add orders app to installed apps** (✓ Already done in settings.py)

2. **Run migrations:**
   ```bash
   cd farmers-market
   python manage.py migrate
   ```

3. **Create test users:**
   ```bash
   python manage.py shell
   ```
   
   In the shell:
   ```python
   from accounts.models import User, FarmerProfile
   
   # Create a farmer
   farmer = User.objects.create_user(
       username='farmer1',
       password='password123',
       role='FARMER'
   )
   FarmerProfile.objects.create(user=farmer, farm_name='Fresh Farm')
   
   # Create a customer
   customer = User.objects.create_user(
       username='customer1',
       password='password123',
       role='CUSTOMER'
   )
   
   # Create a sample product
   from posts.models import Post
   post = Post.objects.create(
       author=farmer,
       title='Organic Tomatoes',
       content='Fresh organic tomatoes',
       price=50.00,
       quantity=100,
       unit='KG'
   )
   ```

4. **Verify models in admin:**
   ```
   http://localhost:8000/admin
   ```
   - Orders app should appear
   - Order and OrderItem models should be visible

### Frontend Setup

The React components are already created:
- `OrdersView.jsx` - Customer order history
- `FarmerOrdersManagement.jsx` - Farmer order management
- API module `orders.js` - API integration

## Testing the System

### Test Scenario 1: Customer Places Order

1. **Login as customer:**
   - Username: `customer1`
   - Password: `password123`

2. **Add items to cart:**
   - Browse products from farmer1
   - Add "Organic Tomatoes" (10 KG) to cart

3. **Proceed to checkout:**
   - Click "Proceed to Checkout"
   - Should see order confirmation with "In Progress" status
   - Order ID should be displayed

4. **Check My Orders:**
   - Navigate to "My Orders" section
   - See order with "⏳ In Progress" badge
   - Order shows items and total amount

### Test Scenario 2: Farmer Approves Order

1. **Login as farmer:**
   - Username: `farmer1`
   - Password: `password123`

2. **Access Order Management:**
   - Go to farmer dashboard/order management
   - Should see pending order from customer1
   - Shows order details and items

3. **Approve order:**
   - Click "Accept Order" button
   - Should see success message
   - Order disappears from pending list

4. **Verify changes:**
   - Check post quantity reduced (100 - 10 = 90)
   - Admin: check Order status changed to APPROVED
   - Customer's cart should be cleared

### Test Scenario 3: Customer Sees Approved Order

1. **Login as customer:**
   - Go to "My Orders"
   - Order status should now show "✅ Approved"
   - Items are confirmed for delivery

### Test Scenario 4: Farmer Rejects Order

1. **Login as customer:**
   - Add new items to cart
   - Checkout

2. **Login as farmer:**
   - Go to Order Management
   - Click "Reject Order" button
   - Enter reason: "Out of stock for this batch"
   - Click "Confirm Rejection"

3. **Login as customer:**
   - Check "My Orders" - status should be "❌ Rejected"
   - See rejection reason
   - Go to cart - items should be back in cart
   - Can modify and checkout again

## API Testing with cURL

### Get Pending Orders (Farmer)
```bash
curl -X GET http://localhost:8000/api/orders/my_pending_orders/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Create Order (Checkout)
```bash
curl -X POST http://localhost:8000/api/orders/checkout/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

### Approve Order
```bash
curl -X POST http://localhost:8000/api/orders/{order_id}/approve/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

### Reject Order
```bash
curl -X POST http://localhost:8000/api/orders/{order_id}/reject/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reason": "Out of stock"}'
```

### Get Customer Orders
```bash
curl -X GET http://localhost:8000/api/orders/my_orders/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Frontend Component Integration

To integrate components into your main app:

### In Dashboard.jsx or App.jsx

```jsx
import OrdersView from './components/OrdersView';
import FarmerOrdersManagement from './components/FarmerOrdersManagement';

// For customers - add to dashboard
<OrdersView />

// For farmers - add to farmer dashboard
{user.role === 'FARMER' && <FarmerOrdersManagement />}
```

## Troubleshooting

### Issue: "Orders app not found"
- Ensure `'orders'` is added to INSTALLED_APPS in settings.py
- Run `python manage.py migrate`

### Issue: API returns 404
- Check that orders URLs are included in main config/urls.py
- Verify endpoint path: `/api/orders/...`

### Issue: Order not appearing in pending
- Check farmer user has FarmerProfile
- Verify product belongs to the farmer
- Check order status is IN_PROGRESS

### Issue: Inventory not reducing after approval
- Check post.quantity is a DecimalField
- Verify order item quantity is being calculated correctly
- Check transaction was committed (no rollback)

## Files Modified/Created

### Backend
- `orders/models.py` - Order and OrderItem models
- `orders/views.py` - OrderViewSet with checkout/approve/reject
- `orders/serializers.py` - Order and OrderItem serializers
- `orders/urls.py` - Order routes
- `orders/admin.py` - Django admin configuration
- `orders/apps.py` - App configuration
- `orders/migrations/0001_initial.py` - Initial migration
- `config/settings.py` - Added 'orders' to INSTALLED_APPS
- `config/urls.py` - Added orders URL include

### Frontend
- `web/src/api/orders.js` - Order API functions
- `web/src/components/OrdersView.jsx` - Customer order view
- `web/src/components/OrdersView.css` - Customer order styling
- `web/src/components/FarmerOrdersManagement.jsx` - Farmer order management
- `web/src/components/FarmerOrdersManagement.css` - Farmer order styling
- `web/src/components/CartView.jsx` - Updated checkout flow
- `web/src/components/CartView.css` - Updated styling

### Documentation
- `CHECKOUT_STAGING_IMPLEMENTATION.md` - Technical documentation

## Next Steps

1. Run migrations
2. Create test users
3. Test the flow manually
4. Integrate components into your main navigation
5. Add real-time notifications (future enhancement)
6. Implement order history persistence
7. Add payment gateway integration

## Support

For issues or questions about the implementation, refer to:
- `CHECKOUT_STAGING_IMPLEMENTATION.md` for technical details
- Component files for code examples
- Django admin interface for data inspection
