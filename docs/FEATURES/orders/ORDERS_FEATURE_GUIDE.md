# Orders Feature - Complete Implementation Guide

## Overview

The Orders feature implements a **checkout staging system** where customers can submit orders and farmers can accept or reject them in real-time.

**Status**: ✅ Production Ready (v1.0)

---

## Feature Workflow

### Customer Flow
1. **Add Items to Cart** - Browse and add farm products
2. **Click Checkout** - Submits order to farmers for approval
3. **Order Status Tracking** - Real-time status updates:
   - ⏳ **IN_PROGRESS** - Awaiting farmer decision
   - ✅ **APPROVED** - Order accepted, inventory reduced
   - ❌ **REJECTED** - Order declined, items returned to cart
   - 🎉 **COMPLETED** - Order fulfilled

### Farmer Flow
1. **View Pending Orders** - Dashboard shows orders awaiting approval
2. **Review Items** - See customer name, items, quantities, and total price
3. **Accept Order** - Approves order and reduces inventory
4. **Reject Order** - Denies order with optional reason explanation
5. **Real-time Updates** - Dashboard refreshes every 3 seconds

---

## User Interface Components

### Customer Components

#### OrdersView.jsx
- **Path**: `web/src/components/OrdersView.jsx`
- **Features**:
  - Displays all customer orders with status badges
  - Real-time polling (5-second intervals)
  - Expandable order details showing all items
  - Color-coded status indicators
  - Order date and total amount display
- **Styling**: `OrdersView.css`

#### CartView.jsx (Updated)
- **Path**: `web/src/components/CartView.jsx`
- **Features**:
  - Cart item management (add, remove, update quantities)
  - New checkout flow → orders instead of direct purchase
  - Order confirmation display after submission
  - Success/rejection message display
  - Links to order history
- **Styling**: `CartView.css`

### Farmer Components

#### FarmerOrdersManagement.jsx
- **Path**: `web/src/components/FarmerOrdersManagement.jsx`
- **Features**:
  - **Accept Order Button** (✅) - One-click approval
  - **Reject Order Button** (❌) - Triggers rejection form
  - **Rejection Reason Form** - Textarea for detailed explanation
  - **Order Details** - Customer name, items, quantities, total
  - **Real-time Updates** - Polls every 3 seconds
  - **Success/Error Messages** - Feedback for all actions
- **Styling**: `FarmerOrdersManagement.css`

---

## API Endpoints

### Base URL
```
http://127.0.0.1:8000/api/
```

### Endpoints Reference

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| `POST` | `/orders/checkout/` | Create order from cart items | Required |
| `GET` | `/orders/my_orders/` | Get customer's all orders | Required |
| `GET` | `/orders/my_pending_orders/` | Get farmer's pending orders | Farmer Only |
| `GET` | `/orders/{id}/` | Get order details | Required |
| `POST` | `/orders/{id}/approve/` | Farmer approves order | Farmer Only |
| `POST` | `/orders/{id}/reject/` | Farmer rejects order | Farmer Only |

### Example Requests

**Checkout Order**
```javascript
POST /orders/checkout/
Content-Type: application/json
Authorization: Bearer {token}

{}  // Empty body - uses authenticated user's cart
```

**Approve Order**
```javascript
POST /orders/{orderId}/approve/
Authorization: Bearer {token}
```

**Reject Order**
```javascript
POST /orders/{orderId}/reject/
Content-Type: application/json
Authorization: Bearer {token}

{
  "reason": "Out of stock"
}
```

---

## Database Models

### Order Model
```python
class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Completed'),
    ]
    
    customer = ForeignKey(User, on_delete=models.CASCADE)
    status = CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    rejection_reason = TextField(blank=True, null=True)
```

### OrderItem Model
```python
class OrderItem(models.Model):
    order = ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    post = ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    farmer = ForeignKey(User, on_delete=models.SET_NULL, null=True)
    quantity = DecimalField(max_digits=10, decimal_places=2)
    price = DecimalField(max_digits=10, decimal_places=2)
    total_price = DecimalField(max_digits=10, decimal_places=2)
    unit = CharField(max_length=50)
```

---

## Key Implementation Details

### Status Transitions
```
PENDING → IN_PROGRESS (on checkout)
IN_PROGRESS → APPROVED (farmer accepts)
IN_PROGRESS → REJECTED (farmer rejects)
APPROVED → COMPLETED (admin/backend marks as complete)
```

### Real-time Updates
- **Customer Dashboard**: Polls every 5 seconds for order status changes
- **Farmer Dashboard**: Polls every 3 seconds for new pending orders
- **Updates Trigger**: Page refresh with latest order data

### Inventory Management
- **On Approval**: Inventory decremented by ordered quantity
- **On Rejection**: Cart items restored for customer to retry
- **Atomic Transactions**: Database transactions prevent race conditions

### Data Type Handling
- **API Returns**: Decimal fields serialized as strings for precision (e.g., "125.50")
- **Frontend Handling**: All numeric values wrapped with `parseFloat()` before formatting
- **Safety Pattern**: `(parseFloat(value) || 0).toFixed(2)` prevents errors

---

## File Structure

```
farmers-market/
├── orders/                           # NEW APP
│   ├── __init__.py
│   ├── models.py                    # Order & OrderItem models
│   ├── views.py                     # API endpoints & business logic
│   ├── serializers.py               # Order serialization
│   ├── urls.py                      # API routes
│   ├── admin.py                     # Django admin integration
│   └── migrations/
│       └── 0001_initial.py          # Create tables

web/
├── src/
│   ├── api/
│   │   └── orders.js                # API client functions
│   └── components/
│       ├── CartView.jsx             # UPDATED - new checkout flow
│       ├── CartView.css
│       ├── OrdersView.jsx           # UPDATED - numeric fixes
│       ├── OrdersView.css
│       ├── FarmerOrdersManagement.jsx  # UPDATED - numeric fixes
│       └── FarmerOrdersManagement.css
```

---

## Testing Checklist

- [ ] Customer can add items to cart
- [ ] Customer can click "Checkout" to create order
- [ ] Order appears in customer's order history with "IN_PROGRESS" status
- [ ] Order appears in farmer's pending orders dashboard
- [ ] Farmer can click "Accept Order" to approve
- [ ] On approval: Order status changes to "APPROVED", inventory updated
- [ ] Farmer can click "Reject Order" to open rejection form
- [ ] Farmer can enter rejection reason and confirm
- [ ] On rejection: Order status changes to "REJECTED", items returned to customer's cart
- [ ] Real-time polling updates both dashboards every 3-5 seconds
- [ ] All prices display correctly (no `.toFixed()` errors)
- [ ] Error messages display for API failures

---

## Troubleshooting

### Common Issues

**Issue**: `TypeError: item.total_price.toFixed is not a function`
- **Cause**: API returns Decimal as string, not number
- **Solution**: ✅ Fixed in v1.0 - all numeric fields use `parseFloat()` conversion

**Issue**: Orders not appearing in farmer dashboard
- **Cause**: User not marked as farmer in database
- **Solution**: Check `is_staff` flag in Django admin

**Issue**: Cart not clearing after successful checkout
- **Cause**: Frontend not updating cart state after order creation
- **Solution**: CartView automatically syncs with backend cart after checkout

---

## Related Documentation

- [API Reference](../GUIDES/API_REFERENCE.md)
- [Database Schema](../COMPONENT_ARCHITECTURE.md)
- [Deployment Guide](../PROJECT_COMPLETION.md)

---

**Last Updated**: January 12, 2026
**Version**: 1.0 - Production Release
**Status**: ✅ Complete
