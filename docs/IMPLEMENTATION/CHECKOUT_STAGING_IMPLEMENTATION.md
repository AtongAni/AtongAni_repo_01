# Checkout Staging System - Implementation Guide

## Overview

The checkout staging system implements an order approval workflow where farmers can review and approve/reject customer orders before they are processed. This ensures inventory control and allows farmers to manage their stock effectively.

## System Flow

```
Customer Checkout → Order Created (IN_PROGRESS) 
                    ↓
                Farmer Reviews
                    ↓
        ┌─────────────┬─────────────┐
        ↓             ↓
    Approve       Reject
        ↓             ↓
   (APPROVED)   Items Return to Cart
                 (REJECTED)
```

## Database Models

### Order Model
- `customer`: ForeignKey to User (the customer who placed the order)
- `status`: CharField with choices:
  - `PENDING`: Order created but not yet viewed by farmer
  - `IN_PROGRESS`: Farmer is reviewing the order
  - `APPROVED`: Farmer approved, inventory reduced, cart cleared
  - `REJECTED`: Farmer rejected, items return to cart
  - `COMPLETED`: Order fully processed
- `created_at`: Timestamp when order was created
- `updated_at`: Timestamp of last update
- `rejection_reason`: Text field for rejection reason if applicable

### OrderItem Model
- `order`: ForeignKey to Order
- `post`: ForeignKey to Post (product being ordered)
- `farmer`: ForeignKey to User (farmer who owns the post)
- `quantity`: Decimal field for ordered quantity
- `price`: Decimal field for price per unit
- `total_price`: Auto-calculated total (price × quantity)
- `unit`: Unit of measurement (KG, G)
- `created_at`: Timestamp

## API Endpoints

### For Customers

#### 1. Create Order (Checkout)
```
POST /api/orders/checkout/
```
Creates an order from cart items with status `IN_PROGRESS`

**Response:**
```json
{
  "message": "Order created and awaiting farmer approval",
  "order": {
    "id": 1,
    "customer_name": "john_doe",
    "status": "IN_PROGRESS",
    "items": [...],
    "total_amount": 500.00,
    "rejection_reason": null,
    "created_at": "2024-01-12T10:30:00Z",
    "updated_at": "2024-01-12T10:30:00Z"
  }
}
```

#### 2. Get All Customer Orders
```
GET /api/orders/my_orders/
```
Returns all orders for the logged-in customer (all statuses)

#### 3. Get Order Detail
```
GET /api/orders/{order_id}/
```
Returns detailed information about a specific order

### For Farmers

#### 1. Get Pending Orders
```
GET /api/orders/my_pending_orders/
```
Returns all orders awaiting this farmer's approval (status = IN_PROGRESS)

#### 2. Approve Order
```
POST /api/orders/{order_id}/approve/
```
Farmer approves an order. This action:
- Reduces post quantity by ordered amount
- Deletes post if quantity reaches 0
- Sets order status to `APPROVED`
- Clears customer's cart items
- Returns order with updated status

**Response:**
```json
{
  "message": "Order approved successfully",
  "order": {
    "id": 1,
    "status": "APPROVED",
    ...
  }
}
```

#### 3. Reject Order
```
POST /api/orders/{order_id}/reject/
```
Farmer rejects an order. This action:
- Sets order status to `REJECTED`
- Returns all items to customer's cart
- Stores rejection reason
- Notifies customer of rejection

**Request Body:**
```json
{
  "reason": "Out of stock for this item"
}
```

**Response:**
```json
{
  "message": "Order rejected. Items returned to customer's cart",
  "order": {
    "id": 1,
    "status": "REJECTED",
    "rejection_reason": "Out of stock for this item",
    ...
  }
}
```

## Frontend Components

### 1. CartView.jsx (Updated)
- Shows shopping cart with items
- Displays "Proceed to Checkout" button
- After checkout, shows order confirmation with status badge
- Polls for order updates

### 2. OrdersView.jsx (New)
**Path:** `web/src/components/OrdersView.jsx`

Features:
- Displays all customer orders
- Shows order status with color-coded badges
- Expandable order details
- Real-time status updates via polling (5 second intervals)
- Displays rejection reason if applicable
- Shows in-progress message while farmer reviews
- Responsive design

Status Colors:
- `IN_PROGRESS`: Orange (⏳)
- `APPROVED`: Green (✅)
- `REJECTED`: Red (❌)
- `COMPLETED`: Blue (🎉)

### 3. FarmerOrdersManagement.jsx (New)
**Path:** `web/src/components/FarmerOrdersManagement.jsx`

Features:
- Lists all pending orders awaiting farmer approval
- Shows customer name and order details
- Displays all items in the order
- Accept/Reject buttons for each order
- Rejection form with reason textarea
- Real-time order list updates via polling (3 second intervals)
- Success/error messages
- Responsive design

## API Module

**Path:** `web/src/api/orders.js`

Functions:
```javascript
getOrders()              // Get customer's orders
getPendingOrders()       // Get pending orders (farmers)
getOrderDetail(orderId)  // Get specific order details
checkoutCart()           // Create order from cart
approveOrder(orderId)    // Farmer approves order
rejectOrder(orderId, reason)  // Farmer rejects with reason
```

## Integration with Cart System

The checkout process has been modified:

**Before:** Direct checkout cleared cart and reduced inventory immediately
**After:** Checkout creates order with IN_PROGRESS status, waits for farmer approval

When an order is approved:
- Cart items are cleared
- Inventory is reduced
- Order status becomes APPROVED

When an order is rejected:
- Order status becomes REJECTED
- Cart items are restored
- Inventory is unaffected

## Key Features

1. **Inventory Protection**: Inventory only changes after farmer approval
2. **Customer Transparency**: Customers can track order status in real-time
3. **Farmer Control**: Farmers can reject orders with explanation
4. **Cart Restoration**: Rejected orders automatically return items to cart
5. **Notification Ready**: System supports future notification integration
6. **Scalable Design**: Handles multiple items from multiple farmers per order

## Usage Instructions

### For Customers

1. Add items to cart
2. Click "Proceed to Checkout"
3. Order is created with status "In Progress"
4. View order in "My Orders" section
5. Wait for farmer approval
6. If approved: Order confirmed, items will be prepared
7. If rejected: Items return to cart with rejection reason

### For Farmers

1. Go to "Order Management" dashboard
2. View all pending orders
3. Review customer order details
4. Click "Accept Order" to approve
   - Inventory reduces, order confirmed
5. Or click "Reject Order" to decline
   - Enter rejection reason
   - Items return to customer's cart

## Database Migrations

Run migrations to create the orders tables:
```bash
python manage.py migrate
```

## Future Enhancements

1. **Notifications**: Email/SMS notifications for order status changes
2. **Order Expiration**: Auto-reject orders not approved within time limit
3. **Partial Approval**: Allow farmers to approve/reject individual items
4. **Order Tracking**: Delivery status tracking
5. **Payment Integration**: Process payment only after approval
6. **Analytics**: Order completion rates by farmer

## Error Handling

The system handles various error scenarios:

- **Insufficient Stock**: If farmer tries to approve but stock is insufficient
- **Unauthorized Access**: Only order owner/farmer can access relevant orders
- **Invalid Status**: Cannot approve/reject orders not in IN_PROGRESS status
- **Empty Reason**: Rejection requires a reason from farmer

## Security Considerations

1. **Authentication**: All endpoints require JWT authentication
2. **Authorization**: 
   - Farmers can only approve orders for their products
   - Customers can only view their own orders
3. **Data Integrity**: Transaction-based operations ensure consistency
4. **Audit Trail**: All order changes are timestamped and tracked
