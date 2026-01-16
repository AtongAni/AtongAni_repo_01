# Simulation Delivery - Implementation Guide

## Overview

This guide documents how to integrate the Simulation Delivery feature into your Farmers Market application. The feature was designed with future real delivery integrations in mind.

## What Was Implemented

### Backend Changes

#### 1. Order Model Updates
**File**: `farmers-market/orders/models.py`

```python
# New status added to ORDER STATUS_CHOICES
'SIMULATION_DELIVERY', 'Simulation Delivery'

# New fields added to Order model
approved_at = models.DateTimeField(blank=True, null=True)
delivery_confirmation_shown_at = models.DateTimeField(blank=True, null=True)
```

**Migration Required**: Yes
```bash
python manage.py makemigrations orders
python manage.py migrate
```

#### 2. Tasks Module (New File)
**File**: `farmers-market/orders/tasks.py`

Handles the 10-second delivery simulation:
```python
def trigger_simulation_delivery(order_id):
    """Simulates 10-second delivery, then updates order status"""
    time.sleep(10)
    order = Order.objects.get(id=order_id)
    if order.status == 'APPROVED':
        order.status = 'SIMULATION_DELIVERY'
        order.delivery_confirmation_shown_at = timezone.now()
        order.save()
```

#### 3. OrderViewSet Updates
**File**: `farmers-market/orders/views.py`

**Modified**: `approve()` endpoint
- Now triggers `trigger_simulation_delivery()` in background thread
- Uses Python's `threading` module (no external dependencies)

**New**: `confirm_received()` endpoint
```python
@action(detail=True, methods=['post'])
def confirm_received(self, request, pk=None):
    """Transitions SIMULATION_DELIVERY → COMPLETED when customer confirms"""
    # Validates customer ownership
    # Validates order is in SIMULATION_DELIVERY status
    # Marks order COMPLETED
```

#### 4. Serializer Updates
**File**: `farmers-market/orders/serializers.py`

Added new fields to serializer output:
- `approved_at`
- `delivery_confirmation_shown_at`

### Frontend Changes

#### 1. OrdersView Component Updates
**File**: `web/src/components/OrdersView.jsx`

**New Features**:
- Auto-detection of SIMULATION_DELIVERY orders
- Automatic modal display
- Delivery confirmation handler

**New State Variables**:
```javascript
const [deliveryModal, setDeliveryModal] = useState({ isOpen: false, orderId: null });
const [confirmingOrder, setConfirmingOrder] = useState(null);
```

**New useEffect**:
```javascript
// Auto-opens delivery confirmation modal when order enters SIMULATION_DELIVERY
useEffect(() => {
    const deliveryOrder = orders.find(order => order.status === 'SIMULATION_DELIVERY');
    if (deliveryOrder && !deliveryModal.isOpen) {
        setDeliveryModal({ isOpen: true, orderId: deliveryOrder.id });
    }
}, [orders, deliveryModal.isOpen]);
```

#### 2. Delivery Confirmation Modal
**File**: `web/src/components/OrdersView.jsx`

New modal UI component with:
- Auto-popup when delivery status detected
- Confirmation button ("Yes, I Received It")
- Error message handling
- Loading state during API call

#### 3. Status Color & Icon Updates
**File**: `web/src/components/OrdersView.jsx`

Added SIMULATION_DELIVERY to status colors and icons:
```javascript
case "SIMULATION_DELIVERY":
    return "🚚";  // Truck emoji
```

#### 4. CSS Styling
**File**: `web/src/components/OrdersView.css`

New styles added:
- `.delivery-modal-overlay`: Backdrop
- `.delivery-modal`: Modal container
- `.modal-header`, `.modal-body`, `.modal-footer`: Modal sections
- `.btn-confirm`, `.btn-cancel`: Action buttons
- `.delivery-note`: Order status note
- `.modal-error`: Error display

#### 5. API Client Update
**File**: `web/src/api/orders.js`

New function:
```javascript
export function confirmOrderReceived(orderId) {
    return api.post(`/api/orders/${orderId}/confirm_received/`);
}
```

## How It Works

### Sequence Diagram

```
Customer             Farmer              Backend             Frontend
   |                   |                    |                   |
   |-- Place Order --->|                    |                   |
   |                   |                    |                   |
   |                   |-- Approve Order -->|                   |
   |                   |                    |                   |
   |                   |<--- OK -------     |                   |
   |                   |                    |-- Background     |
   |                   |                    |   Thread Start   |
   |                   |                    |                   |
   |                   |                    |   (10 sec sleep)  |
   |                   |                    |                   |
   | <--- Poll (5s) ---|---- Status: APPROVED -------->|
   |                   |                    |                   |
   | <--- Poll (5s) ---|---- Status: SIMULATION_DELIVERY -->|
   |                   |                    |                   |
   |                   |                    |        Modal |
   |                   |                    |        Popup |
   |                   |                    |                   |
   | Click "Confirm" --|-------------------|---------->|
   |                   |                    |           |
   | <--- Post --------|-- Confirm Received -->|
   |                   |                    |           |
   | <--- OK ------    |<--- Status: COMPLETED --|
   |                   |                    |
```

### Step-by-Step Flow

1. **Customer places order**: Status = `IN_PROGRESS`
2. **Farmer approves order**:
   - Status = `APPROVED`
   - Background thread starts (10-second timer)
3. **10 seconds pass** (in background):
   - Status = `SIMULATION_DELIVERY`
   - `delivery_confirmation_shown_at` timestamp set
4. **Frontend detects SIMULATION_DELIVERY**:
   - Modal automatically pops up
   - Asks customer: "Have you received your order?"
5. **Customer confirms**:
   - API call: `POST /api/orders/{id}/confirm_received/`
   - Status = `COMPLETED`
   - Modal closes

## Database Migrations

After implementing these changes, you need to create and run migrations:

```bash
# Create migration
python manage.py makemigrations orders

# View migration
python manage.py showmigrations orders

# Apply migration
python manage.py migrate orders
```

**Migration will add**:
- `SIMULATION_DELIVERY` to status choices (no schema change, just choice expansion)
- `approved_at` column to orders table
- `delivery_confirmation_shown_at` column to orders table

## API Changes

### New Endpoint: Confirm Order Received

**Request**:
```
POST /api/orders/{orderId}/confirm_received/
Authorization: Bearer <token>
Content-Type: application/json
{}
```

**Success Response (200 OK)**:
```json
{
  "message": "Order confirmed as received",
  "order": {
    "id": 1,
    "customer_name": "john_doe",
    "status": "COMPLETED",
    "items": [...],
    "total_amount": "500.00",
    "approved_at": "2026-01-16T12:00:00Z",
    "delivery_confirmation_shown_at": "2026-01-16T12:00:10Z",
    "created_at": "2026-01-16T11:55:00Z",
    "updated_at": "2026-01-16T12:00:20Z"
  }
}
```

**Error Cases**:

1. **Not the order owner** (403):
```json
{
  "error": "You are not authorized to confirm this order"
}
```

2. **Order not in SIMULATION_DELIVERY status** (400):
```json
{
  "error": "Cannot confirm order with status: APPROVED. Order must be in delivery status."
}
```

3. **Order not found** (404): Standard 404 response

## Testing the Feature

### Manual Testing Checklist

- [ ] Create test customer and farmer accounts
- [ ] Add products as farmer
- [ ] Add product to cart as customer
- [ ] Checkout as customer
- [ ] Approve order as farmer
- [ ] Observe backend: Thread launches
- [ ] Wait ~10 seconds
- [ ] Refresh customer orders page
- [ ] Verify status changed to `SIMULATION_DELIVERY`
- [ ] Modal should auto-popup
- [ ] Click "Yes, I Received It"
- [ ] Verify API call succeeds
- [ ] Verify status changed to `COMPLETED`
- [ ] Modal closes automatically

### API Testing

**Using cURL**:
```bash
# Get orders (check for SIMULATION_DELIVERY)
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/orders/my_orders/

# Confirm delivery
curl -X POST \
  -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/orders/1/confirm_received/
```

**Using Python requests**:
```python
import requests

headers = {"Authorization": f"Bearer {token}"}

# Get orders
response = requests.get('http://localhost:8000/api/orders/my_orders/', headers=headers)
orders = response.json()

# Find SIMULATION_DELIVERY order
delivery_order = next((o for o in orders if o['status'] == 'SIMULATION_DELIVERY'), None)

if delivery_order:
    # Confirm delivery
    response = requests.post(
        f'http://localhost:8000/api/orders/{delivery_order["id"]}/confirm_received/',
        headers=headers
    )
    print(response.json())
```

## Configuration

### Adjust Simulation Delay

**Current**: 10 seconds (hardcoded)

**To Change**, edit `farmers-market/orders/tasks.py`:
```python
def trigger_simulation_delivery(order_id):
    time.sleep(10)  # ← Change this value
```

### Adjust Frontend Polling Interval

**Current**: 5 seconds

**To Change**, edit `web/src/components/OrdersView.jsx`:
```javascript
const interval = setInterval(loadOrders, 5000);  // ← Change this value
```

Smaller values = more responsive (higher server load)
Larger values = less responsive (lower server load)

## Troubleshooting

### Problem: SIMULATION_DELIVERY status never appears

**Possible Causes**:
1. Backend thread not starting - check approve endpoint logs
2. Frontend polling interval too long - increase frequency
3. Database not migrated - run migrations
4. Browser cache - clear cache and reload

**Solution**:
```bash
# Check Django logs
tail -f logs/django.log

# Verify database migration
python manage.py showmigrations orders

# Check database directly
python manage.py dbshell
SELECT status, COUNT(*) FROM orders_order GROUP BY status;
```

### Problem: Modal doesn't auto-open

**Possible Causes**:
1. JavaScript error - check browser console
2. OrdersView component not mounted
3. React state update issue

**Solution**:
```javascript
// Add debugging in OrdersView.jsx
useEffect(() => {
    console.log('Orders loaded:', orders);
    const deliveryOrder = orders.find(o => o.status === 'SIMULATION_DELIVERY');
    console.log('Delivery order found:', deliveryOrder);
    
    if (deliveryOrder && !deliveryModal.isOpen) {
        console.log('Opening modal for order', deliveryOrder.id);
        setDeliveryModal({ isOpen: true, orderId: deliveryOrder.id });
    }
}, [orders, deliveryModal.isOpen]);
```

### Problem: confirm_received returns 400 "Order not in delivery status"

**Possible Causes**:
1. Order transitioned past SIMULATION_DELIVERY
2. Race condition - order updated by another process
3. Stale data - frontend didn't refresh

**Solution**:
```javascript
// Reload orders before confirming
await loadOrders();
```

## Performance Considerations

### Threading Concerns

Uses Python's `threading` module:
- **Pros**: No external dependencies, simple, works well for light load
- **Cons**: Threads die if process restarts, no persistence

**For Production**, consider:
```python
# Option 1: Celery (if already using)
from celery import shared_task
import time

@shared_task
def trigger_simulation_delivery(order_id):
    time.sleep(10)
    # ... update order

# In approve view:
trigger_simulation_delivery.apply_async(args=(order.id,), countdown=10)
```

```python
# Option 2: Django-RQ
import django_rq

queue = django_rq.get_queue('default')
queue.enqueue_in(timedelta(seconds=10), 
                 trigger_simulation_delivery, 
                 order_id=order.id)
```

### Database Load

- Order polling every 5 seconds per customer session
- **For 100 customers**: ~20 queries/second (manageable)
- **For 1000 customers**: ~200 queries/second (consider caching)

**Optimization if needed**:
```python
# Use select_related/prefetch_related
queryset = Order.objects.filter(customer=user).prefetch_related('items__post')

# Add database query caching
from django.views.decorators.cache import cache_page

@cache_page(1)  # Cache for 1 second
def get_orders(self, request):
    ...
```

## Future: Integrating Real Delivery

When ready to implement actual delivery:

1. **Update tasks.py**:
   - Replace `time.sleep(10)` with real delivery API calls
   - Call your delivery provider (Grab, GoFood, custom API, etc.)
   - Store delivery tracking ID

2. **Update confirm_received endpoint**:
   - Add validation that delivery is actually complete
   - Check delivery status from provider
   - Update order data with delivery confirmation details

3. **No frontend changes needed** - everything else stays the same!

Example integration:
```python
# tasks.py - Updated with real delivery provider

from delivery_providers import DDP  # Third-party delivery API

def trigger_simulation_delivery(order_id):
    order = Order.objects.get(id=order_id)
    
    # Call real delivery provider
    try:
        delivery = DDP.schedule_delivery(
            order_id=order.id,
            customer_address=order.customer.address,
            pickup_location=order.items[0].farmer.location
        )
        
        # Store delivery tracking info
        order.delivery_tracking_id = delivery.tracking_id
        order.delivery_provider = 'DDP'
        order.status = 'SIMULATION_DELIVERY'  # Now real delivery
        order.delivery_confirmation_shown_at = timezone.now()
        order.save()
        
    except DeliveryProviderError as e:
        logger.error(f"Delivery failed for order {order_id}: {e}")
        # Fallback: keep order in APPROVED status
```

## Summary

The Simulation Delivery feature is now fully integrated into your Farmers Market application. It provides:

✅ 10-second simulated delivery window  
✅ Automatic customer confirmation modal  
✅ Complete order status flow (APPROVED → SIMULATION_DELIVERY → COMPLETED)  
✅ Easy-to-replace architecture for real delivery integration  
✅ No external dependencies (uses Python threading)  

**Next Steps**:
1. Run database migrations
2. Test the complete flow manually
3. Deploy to production
4. Monitor order completion rates
5. When ready, integrate real delivery provider
