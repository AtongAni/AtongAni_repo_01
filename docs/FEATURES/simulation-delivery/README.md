# Simulation Delivery Feature

## Overview

The **Simulation Delivery** feature is a placeholder order state that bridges the farmer approval step and customer order completion. It simulates a 10-second delivery window, after which customers are prompted to confirm they have received their order.

This feature is designed to be easily replaced with real delivery functionality (GPS tracking, third-party delivery APIs, etc.) without disrupting the order flow or requiring significant refactoring.

## Purpose

- **Simulate Delivery Process**: Provides a 10-second middle event between farmer approval and customer confirmation
- **Easy Integration Point**: Structure allows seamless replacement with real delivery APIs
- **Clean Architecture**: Keeps order flow logic organized and maintainable
- **Placeholder Pattern**: Documents exactly where production delivery code should be integrated

## Order Status Flow

```
PENDING → IN_PROGRESS → APPROVED → SIMULATION_DELIVERY → COMPLETED
                                        ↓
                                    (10 seconds)
                                        ↓
                                   Customer confirms
```

### Status Definitions

| Status | Description | Duration |
|--------|-------------|----------|
| PENDING | Order created (internal state) | - |
| IN_PROGRESS | Order placed, awaiting farmer approval | Variable |
| APPROVED | Farmer approved order and reduced inventory | Variable |
| **SIMULATION_DELIVERY** | **Order in simulated delivery state** | **10 seconds** |
| COMPLETED | Customer confirmed receipt | - |
| REJECTED | Farmer rejected order, items returned to cart | - |

## Technical Implementation

### Backend Components

#### 1. **Order Model** (`farmers-market/orders/models.py`)

```python
STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('IN_PROGRESS', 'In Progress'),
    ('APPROVED', 'Approved'),
    ('SIMULATION_DELIVERY', 'Simulation Delivery'),  # NEW
    ('COMPLETED', 'Completed'),
    ('REJECTED', 'Rejected'),
]
```

**New Fields**:
- `approved_at`: Timestamp when farmer approved the order
- `delivery_confirmation_shown_at`: Timestamp when order entered SIMULATION_DELIVERY status

#### 2. **Tasks Module** (`farmers-market/orders/tasks.py`)

The `trigger_simulation_delivery()` function handles the 10-second delay:

```python
def trigger_simulation_delivery(order_id):
    """
    Triggers simulation delivery after 10 seconds of order approval.
    
    When implementing real delivery:
    - Replace sleep() with actual delivery logic
    - Keep the status update and timestamp recording
    - Maintain the customer confirmation flow
    """
    time.sleep(10)  # ← REPLACE THIS WITH REAL DELIVERY LOGIC
    
    order = Order.objects.get(id=order_id)
    if order.status == 'APPROVED':
        order.status = 'SIMULATION_DELIVERY'
        order.delivery_confirmation_shown_at = timezone.now()
        order.save()
```

#### 3. **API Endpoints** (`farmers-market/orders/views.py`)

##### Approve Endpoint (Updated)
- **URL**: `POST /api/orders/{id}/approve/`
- **What's New**: Launches background thread to trigger simulation delivery after 10 seconds
- **Implementation**:
  ```python
  delivery_thread = threading.Thread(
      target=trigger_simulation_delivery,
      args=(order.id,),
      daemon=True
  )
  delivery_thread.start()
  ```

##### New: Confirm Received Endpoint
- **URL**: `POST /api/orders/{id}/confirm_received/`
- **Method**: POST
- **Authentication**: Required (customer only)
- **Purpose**: Customer confirms they received the order
- **Request Body**: Empty
- **Response**: Updated order with status `COMPLETED`
- **Status Code**: 200 OK

```python
@action(detail=True, methods=['post'])
def confirm_received(self, request, pk=None):
    """Customer confirms order receipt - SIMULATION_DELIVERY → COMPLETED"""
    order = self.get_object()
    
    if order.customer != request.user:
        return Response({'error': 'Not authorized'}, status=403)
    
    if order.status != 'SIMULATION_DELIVERY':
        return Response({'error': 'Order not in delivery'}, status=400)
    
    order.status = 'COMPLETED'
    order.save()
    return Response({'order': serializer.data})
```

### Frontend Components

#### OrdersView Component (`web/src/components/OrdersView.jsx`)

**New Features**:
- `SIMULATION_DELIVERY` status detection
- Auto-popup confirmation modal
- Delivery confirmation handler

**Key States**:
```javascript
const [deliveryModal, setDeliveryModal] = useState({ 
  isOpen: false, 
  orderId: null 
});
const [confirmingOrder, setConfirmingOrder] = useState(null);
```

**Auto-Detection Logic**:
```javascript
useEffect(() => {
  const deliveryOrder = orders.find(order => order.status === 'SIMULATION_DELIVERY');
  if (deliveryOrder && !deliveryModal.isOpen) {
    setDeliveryModal({ isOpen: true, orderId: deliveryOrder.id });
  }
}, [orders, deliveryModal.isOpen]);
```

#### Delivery Confirmation Modal

**Features**:
- Automatically appears when order enters SIMULATION_DELIVERY
- Can be dismissed without confirming (confirmation requested on next load)
- Shows order ID and confirmation prompt
- Loading state during confirmation
- Error handling and display

**UI Elements**:
- Delivery icon (🚚)
- Confirmation button ("Yes, I Received It")
- Close button
- Error message display

### API Client (`web/src/api/orders.js`)

```javascript
export function confirmOrderReceived(orderId) {
  return api.post(`/api/orders/${orderId}/confirm_received/`);
}
```

### Styling (`web/src/components/OrdersView.css`)

New CSS classes for delivery modal:
- `.delivery-modal-overlay`: Dark background overlay
- `.delivery-modal`: Modal container
- `.modal-header`, `.modal-body`, `.modal-footer`: Modal sections
- `.btn-confirm`, `.btn-cancel`: Action buttons
- `.delivery-note`: Order card note styling
- `.modal-error`: Error message styling

## Data Flow

### 1. Farmer Approves Order

```
POST /api/orders/{id}/approve/
↓
Order model: status = 'APPROVED'
↓
Launch background thread: trigger_simulation_delivery(order.id)
↓
Response: {"message": "Order approved successfully", "order": {...}}
```

### 2. 10-Second Simulation Delivery (Background)

```
Thread sleeps for 10 seconds
↓
Fetch order by ID
↓
Check if still in 'APPROVED' status
↓
Update: status = 'SIMULATION_DELIVERY'
↓
Record: delivery_confirmation_shown_at = now()
↓
Order auto-detected by frontend polling (5-second interval)
```

### 3. Frontend Detection & Modal

```
OrdersView polls /api/orders/my_orders/ (5-second interval)
↓
useEffect detects SIMULATION_DELIVERY status
↓
Automatically open delivery confirmation modal
↓
Display: "Have you received your order?"
```

### 4. Customer Confirms Receipt

```
Click "Yes, I Received It"
↓
POST /api/orders/{id}/confirm_received/
↓
Order model: status = 'COMPLETED'
↓
Frontend reload orders
↓
Order shows 🎉 COMPLETED status
↓
Modal closes
```

## Replacing with Real Delivery

When implementing actual delivery functionality (GPS tracking, third-party APIs, etc.):

### Step 1: Update `tasks.py`

```python
# BEFORE (current)
def trigger_simulation_delivery(order_id):
    time.sleep(10)  # Simulate
    order.status = 'SIMULATION_DELIVERY'

# AFTER (example with GPS delivery)
def trigger_simulation_delivery(order_id):
    order = Order.objects.get(id=order_id)
    
    # Call actual delivery API
    delivery_response = integrate_with_delivery_provider(order)
    
    if delivery_response.success:
        order.delivery_tracking_id = delivery_response.tracking_id
        order.status = 'SIMULATION_DELIVERY'  # Now represents real delivery
        order.delivery_confirmation_shown_at = timezone.now()
        order.save()
    else:
        # Handle delivery provider error
        log_error(f"Delivery failed for order {order_id}")
```

### Step 2: Update `confirm_received` endpoint

```python
@action(detail=True, methods=['post'])
def confirm_received(self, request, pk=None):
    order = self.get_object()
    
    if order.status != 'SIMULATION_DELIVERY':
        return Response({'error': 'Order not in delivery'}, status=400)
    
    # NEW: Verify delivery completion if using real delivery provider
    # Example: Check if package was delivered at customer location
    # if not verify_delivery_complete(order.delivery_tracking_id):
    #     return Response({'error': 'Delivery not yet complete'}, status=400)
    
    order.status = 'COMPLETED'
    order.save()
    return Response({'order': serializer.data})
```

### Step 3: No Frontend Changes Required!

The frontend modal and order flow remain completely unchanged. The modal will automatically work with real delivery data.

## Configuration & Tuning

### Simulation Delivery Delay

Currently hardcoded to 10 seconds in `tasks.py`:

```python
time.sleep(10)
```

To make it configurable:

```python
# settings.py
SIMULATION_DELIVERY_DELAY_SECONDS = 10

# tasks.py
def trigger_simulation_delivery(order_id):
    from django.conf import settings
    delay = settings.SIMULATION_DELIVERY_DELAY_SECONDS
    time.sleep(delay)
```

### Frontend Polling Interval

Currently 5 seconds in `OrdersView.jsx`:

```javascript
const interval = setInterval(loadOrders, 5000);  // 5 seconds
```

To reduce latency, adjust the interval (lower = more frequent polling):

```javascript
const interval = setInterval(loadOrders, 2000);  // 2 seconds (more responsive)
```

## Error Handling

### Backend

- **Order not found**: Silently ignored (order was deleted)
- **Order status mismatch**: Skips update (race condition handled)
- **Database error**: Unhandled (should log and monitor)

### Frontend

- **API errors**: Displayed in modal error section
- **Network timeout**: User can retry
- **Modal dismiss**: Confirmation requested on next poll

## Testing

### Manual Testing Steps

1. **Create and checkout order** as customer
2. **Approve order** as farmer
3. **Wait 10 seconds** - observe order status changes to SIMULATION_DELIVERY
4. **Modal appears** automatically
5. **Click "Yes, I Received It"** - order marks COMPLETED

### Automated Testing

```python
# tests.py
def test_simulation_delivery_triggers(self):
    order = Order.objects.create(customer=customer, status='APPROVED')
    
    trigger_simulation_delivery(order.id)
    
    order.refresh_from_db()
    assert order.status == 'SIMULATION_DELIVERY'
    assert order.delivery_confirmation_shown_at is not None

def test_confirm_received(self):
    order = Order.objects.create(
        customer=customer, 
        status='SIMULATION_DELIVERY'
    )
    
    response = client.post(f'/api/orders/{order.id}/confirm_received/')
    
    assert response.status_code == 200
    order.refresh_from_db()
    assert order.status == 'COMPLETED'
```

## Related Documentation

- [Order Flow Documentation](../orders/README.md)
- [Farmer Order Management](../orders/FARMER_ORDERS.md)
- [API Reference - Orders Endpoints](../../GUIDES/API_REFERENCE.md)
- [Backend Integration Guide](../../IMPLEMENTATION/BACKEND_INTEGRATION.md)

## Summary

The Simulation Delivery feature provides:
- ✅ Clean placeholder for delivery functionality
- ✅ 10-second simulated delivery window
- ✅ Easy-to-replace architecture
- ✅ Complete order status flow
- ✅ Automatic customer confirmation modal
- ✅ Well-documented integration points

This design ensures that upgrading to real delivery providers requires **minimal code changes** and **zero frontend modifications**.
