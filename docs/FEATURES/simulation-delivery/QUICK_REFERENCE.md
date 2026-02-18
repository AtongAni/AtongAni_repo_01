# Simulation Delivery - Quick Reference

## What is Simulation Delivery?

A 10-second placeholder state between farmer approval and customer order confirmation. **Easy to replace with real delivery later.**

## Order Status Flow

```
PENDING → IN_PROGRESS → APPROVED → [10 SECONDS] → SIMULATION_DELIVERY → COMPLETED
```

## Key Files Modified/Created

| File | Change | Type |
|------|--------|------|
| `farmers-market/orders/models.py` | Added SIMULATION_DELIVERY status + 2 new timestamp fields | Modified |
| `farmers-market/orders/tasks.py` | New file with trigger_simulation_delivery() function | Created |
| `farmers-market/orders/views.py` | Updated approve(), added confirm_received() | Modified |
| `farmers-market/orders/serializers.py` | Added new fields to serializer | Modified |
| `web/src/components/OrdersView.jsx` | Added delivery modal + auto-detection logic | Modified |
| `web/src/components/OrdersView.css` | Added modal styling | Modified |
| `web/src/api/orders.js` | Added confirmOrderReceived() function | Modified |

## New Database Fields

```sql
ALTER TABLE orders_order ADD COLUMN approved_at DATETIME;
ALTER TABLE orders_order ADD COLUMN delivery_confirmation_shown_at DATETIME;
```

## New API Endpoint

**Confirm Order Received**
```
POST /api/orders/{orderId}/confirm_received/
Authorization: Required
Status Transition: SIMULATION_DELIVERY → COMPLETED
Response: Updated order JSON
```

## Customer Flow

1. ✅ Customer places order
2. ✅ Farmer approves
3. 🚚 Wait 10 seconds (background)
4. 📱 Modal pops up: "Have you received your order?"
5. ✅ Customer clicks "Yes, I Received It"
6. 🎉 Order marked COMPLETED

## Developer Integration Points

### When to replace "Simulation Delivery"

1. **Integrate real delivery provider** (Grab, GoFood, custom API)
   - Edit: `farmers-market/orders/tasks.py`
   - Replace: `time.sleep(10)` with actual delivery API call
   - Status name stays: `SIMULATION_DELIVERY`

2. **Add delivery verification** in confirm_received
   - Edit: `farmers-market/orders/views.py` → `confirm_received()`
   - Add: Check if delivery actually complete

3. **Frontend changes**: NONE! Modal works unchanged

### Example Real Delivery Integration

```python
# tasks.py - BEFORE (current)
def trigger_simulation_delivery(order_id):
    time.sleep(10)
    order.status = 'SIMULATION_DELIVERY'

# tasks.py - AFTER (example)
def trigger_simulation_delivery(order_id):
    delivery = MyDeliveryProvider.schedule(order_id)
    order.delivery_tracking_id = delivery.id
    order.status = 'SIMULATION_DELIVERY'  # Still works with real delivery!
```

## Testing

### Quick Manual Test

```bash
# 1. Approve an order as farmer
# 2. Wait 10 seconds
# 3. Refresh customer orders page
# 4. Modal should appear
# 5. Click confirmation button
# 6. Order should be COMPLETED
```

### API Test

```bash
curl -X POST \
  -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/orders/1/confirm_received/
```

## Status Codes Reference

| Code | Scenario |
|------|----------|
| 200 | Successfully confirmed delivery |
| 400 | Order not in SIMULATION_DELIVERY status |
| 403 | Not the order customer (unauthorized) |
| 404 | Order not found |

## Configuration

### Change 10-second delay

Edit: `farmers-market/orders/tasks.py`
```python
time.sleep(10)  # Change this number
```

### Change frontend polling frequency

Edit: `web/src/components/OrdersView.jsx`
```javascript
setInterval(loadOrders, 5000)  // milliseconds
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| SIMULATION_DELIVERY never appears | Check backend thread in approve endpoint, verify database migrated |
| Modal doesn't pop up | Check browser console for JS errors, verify polling interval |
| confirm_received returns 400 | Reload orders first, ensure order is in SIMULATION_DELIVERY |
| Migrations failing | Check ORDER status choices already exist in database |

## Dependencies

- ✅ No new external packages
- ✅ Uses Python's built-in `threading` module
- ✅ Works with existing Django REST Framework setup

## Documentation Files

- **README.md** - Full feature overview and architecture
- **IMPLEMENTATION.md** - Detailed implementation guide and integration
- **QUICK_REFERENCE.md** - This file

## Key Timestamps

- `approved_at` - When farmer approved the order
- `delivery_confirmation_shown_at` - When order entered SIMULATION_DELIVERY

These are useful for analytics:
- Average approval time = `approved_at - created_at`
- Average delivery time = `updated_at - delivery_confirmation_shown_at`

---

**Need more details?** See README.md or IMPLEMENTATION.md
