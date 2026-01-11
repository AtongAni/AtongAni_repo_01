# Orders Feature Documentation Index

**Feature**: Checkout Staging System with Farmer Approval  
**Status**: ✅ Production Ready (v1.0)  
**Last Updated**: January 12, 2026  

---

## Quick Start

New to the Orders feature? Start here:

1. **[ORDERS_FEATURE_GUIDE.md](ORDERS_FEATURE_GUIDE.md)** - Complete feature overview and workflow
2. **[ORDERS_FARMER_UI_GUIDE.md](ORDERS_FARMER_UI_GUIDE.md)** - How farmers accept/reject orders
3. **[ORDERS_CUSTOMER_UI_GUIDE.md](ORDERS_CUSTOMER_UI_GUIDE.md)** - How customers track orders

---

## Documentation Files

### Core Documentation

#### [ORDERS_FEATURE_GUIDE.md](ORDERS_FEATURE_GUIDE.md)
**Complete feature overview**
- Feature workflow (customer & farmer flows)
- User interface components
- API endpoints reference
- Database models
- Key implementation details
- Data type handling
- File structure
- Testing checklist
- Troubleshooting guide
- Related documentation links

#### [ORDERS_FARMER_UI_GUIDE.md](ORDERS_FARMER_UI_GUIDE.md)
**Farmer dashboard UI documentation**
- Interface layout and design
- Action buttons (Accept/Reject)
- Rejection form with reason input
- Real-time order updates (3-second polling)
- Data display format
- Mobile responsiveness
- Color scheme and styling
- Keyboard navigation
- Common workflows
- Accessibility features
- Performance notes

#### [ORDERS_CUSTOMER_UI_GUIDE.md](ORDERS_CUSTOMER_UI_GUIDE.md)
**Customer order history UI documentation**
- Order list view (collapsed/expanded)
- Status badges with icons and colors
  - ⏳ IN_PROGRESS (blue)
  - ✅ APPROVED (green)
  - ❌ REJECTED (red)
  - 🎉 COMPLETED (yellow)
- Order card components
- Real-time updates (5-second polling)
- Expandable order details
- Rejection reason display
- Mobile responsiveness
- Interaction patterns
- Color scheme and styling
- Use cases and workflows

#### [ORDERS_API_REFERENCE.md](ORDERS_API_REFERENCE.md)
**Complete API endpoint documentation**
- Base URL and authentication
- 6 API endpoints with detailed documentation
  - GET /orders/my_orders/ (customer history)
  - GET /orders/my_pending_orders/ (farmer pending)
  - GET /orders/{id}/ (order details)
  - POST /orders/checkout/ (create order)
  - POST /orders/{id}/approve/ (farmer approves)
  - POST /orders/{id}/reject/ (farmer rejects)
- Request/response examples for each endpoint
- Data types and models
- Error responses
- Rate limiting
- Authentication
- CORS headers
- Code examples (JavaScript/Fetch)
- Pagination support

#### [ORDERS_IMPLEMENTATION_CHECKLIST.md](ORDERS_IMPLEMENTATION_CHECKLIST.md)
**Implementation progress tracking**
- Backend implementation checklist
- Frontend implementation checklist
- API module checklist
- Integration and testing checklist
- Documentation checklist
- Known limitations and future improvements
- Deployment checklist
- Status: ✅ Complete

---

## Feature Workflow Summary

### Customer Workflow
1. **Add to Cart** → Browse and add farm products
2. **Checkout** → Clicks checkout button
3. **Order Created** → Order status = IN_PROGRESS
4. **Wait for Approval** → Farmer reviews order (⏳)
5. **Order Approved** → Status = APPROVED (✅)
   - OR Order Rejected → Status = REJECTED (❌)
6. **View in History** → See all orders with status

### Farmer Workflow
1. **View Dashboard** → See pending orders
2. **Review Order** → Check customer, items, prices
3. **Make Decision**:
   - **Accept** → Click ✅ Accept Order button
   - **Reject** → Click ❌ Reject Order button
4. **On Rejection** → Enter reason in form
5. **Confirmation** → Order status updated
6. **Real-time** → Dashboard updates every 3 seconds

---

## Database Schema

### Order Model
```
id          → Unique order identifier
customer    → FK to User (customer who placed order)
status      → Choice field (PENDING, IN_PROGRESS, APPROVED, REJECTED, COMPLETED)
created_at  → Timestamp when order created
updated_at  → Timestamp when order last updated
rejection_reason → Text field (optional, only if rejected)
```

### OrderItem Model
```
id          → Unique order item identifier
order       → FK to Order (which order this item belongs to)
post        → FK to Post (the product)
farmer      → FK to User (farmer who sells the product)
quantity    → Decimal (how many units ordered)
price       → Decimal (unit price at time of order)
total_price → Decimal (quantity × price)
unit        → String (kg, bundles, pieces, etc.)
```

---

## Key Features

✅ **Checkout Staging System**
- Orders don't process immediately
- Farmers review and approve/reject
- Real-time status tracking

✅ **Farmer Approval**
- Dashboard shows pending orders
- One-click accept button
- Rejection form with reason explanation
- Real-time updates every 3 seconds

✅ **Customer Order History**
- View all placed orders
- See status with color-coded badges
- Expandable order details
- Real-time status updates every 5 seconds
- Rejection reasons displayed

✅ **Inventory Management**
- Automatic reduction on approval
- Automatic restoration on rejection
- Cart restoration for rejected orders

✅ **Real-time Updates**
- No manual refresh needed
- Automatic polling
- Immediate status changes

✅ **Responsive Design**
- Works on desktop, tablet, mobile
- Touch-friendly buttons
- Readable on all screen sizes

---

## API Endpoints Quick Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/orders/checkout/` | Create order from cart |
| GET | `/orders/my_orders/` | Get customer's orders |
| GET | `/orders/my_pending_orders/` | Get farmer's pending approvals |
| GET | `/orders/{id}/` | Get order details |
| POST | `/orders/{id}/approve/` | Farmer approves order |
| POST | `/orders/{id}/reject/` | Farmer rejects order |

For detailed documentation, see [ORDERS_API_REFERENCE.md](ORDERS_API_REFERENCE.md)

---

## File Structure

```
docs/FEATURES/orders/                         ← You are here
├── README.md                                  ← This file
├── ORDERS_FEATURE_GUIDE.md                   ← Complete overview
├── ORDERS_IMPLEMENTATION_CHECKLIST.md        ← Progress tracking
├── ORDERS_API_REFERENCE.md                   ← API endpoints
├── ORDERS_FARMER_UI_GUIDE.md                 ← Farmer UI
└── ORDERS_CUSTOMER_UI_GUIDE.md               ← Customer UI

farmers-market/orders/                        ← Backend app
├── models.py                                 ← Order & OrderItem models
├── views.py                                  ← API endpoints
├── serializers.py                            ← Order serialization
├── urls.py                                   ← API routes
├── admin.py                                  ← Django admin
└── migrations/

web/src/
├── api/orders.js                             ← API client
└── components/
    ├── CartView.jsx                          ← Updated for checkout flow
    ├── OrdersView.jsx                        ← Customer order history
    └── FarmerOrdersManagement.jsx            ← Farmer dashboard
```

---

## Testing & Verification

### Test Scenarios Completed ✅
- [x] Customer checkout flow
- [x] Farmer approval flow
- [x] Farmer rejection flow with reason
- [x] Order status display and updates
- [x] Real-time polling (3s farmer, 5s customer)
- [x] Cart clearing on approval
- [x] Cart restoration on rejection
- [x] Numeric data type handling
- [x] Mobile responsiveness
- [x] Error handling

---

## Troubleshooting

### Common Issues & Solutions

**Issue**: `TypeError: item.total_price.toFixed is not a function`
- **Root Cause**: API returns Decimal as string
- **Solution**: ✅ Fixed in v1.0 - all numeric fields use parseFloat()

**Issue**: Orders not appearing in farmer dashboard
- **Root Cause**: User not marked as farmer
- **Solution**: Check `is_staff` flag in Django admin

**Issue**: Cart not clearing after checkout
- **Root Cause**: Frontend not syncing with backend
- **Solution**: ✅ Fixed - CartView auto-syncs after order creation

See [ORDERS_FEATURE_GUIDE.md#Troubleshooting](ORDERS_FEATURE_GUIDE.md#troubleshooting) for more details.

---

## Useful Links

- **Backend Code**: [farmers-market/orders/](../../farmers-market/orders/)
- **Frontend Code**: [web/src/components/](../../web/src/components/)
- **API Client**: [web/src/api/orders.js](../../web/src/api/orders.js)
- **Main Docs**: [Parent Documentation](../)

---

## Version History

### v1.0 (January 12, 2026) ✅
- ✅ Initial implementation complete
- ✅ All API endpoints working
- ✅ Farmer UI with accept/reject
- ✅ Customer UI with status tracking
- ✅ Real-time polling
- ✅ Numeric data type fixes
- ✅ Comprehensive documentation
- **Status**: Production Ready

### Future Versions
- v1.1: WebSocket support for real-time updates
- v2.0: Order fulfillment tracking
- v2.0: Customer notifications
- v2.0: Bulk actions for farmers

---

## Getting Help

### Documentation Resources
1. **Getting Started** → Start with [ORDERS_FEATURE_GUIDE.md](ORDERS_FEATURE_GUIDE.md)
2. **User Guides** → See [ORDERS_FARMER_UI_GUIDE.md](ORDERS_FARMER_UI_GUIDE.md) or [ORDERS_CUSTOMER_UI_GUIDE.md](ORDERS_CUSTOMER_UI_GUIDE.md)
3. **API Integration** → Check [ORDERS_API_REFERENCE.md](ORDERS_API_REFERENCE.md)
4. **Troubleshooting** → See [ORDERS_FEATURE_GUIDE.md#Troubleshooting](ORDERS_FEATURE_GUIDE.md#troubleshooting)

### Common Questions
- **How do farmers approve orders?** → See [ORDERS_FARMER_UI_GUIDE.md#Accept-Order-Button](ORDERS_FARMER_UI_GUIDE.md#accept-order-button)
- **How do customers track orders?** → See [ORDERS_CUSTOMER_UI_GUIDE.md#Real-Time-Updates](ORDERS_CUSTOMER_UI_GUIDE.md#real-time-updates)
- **What happens when orders are rejected?** → See [ORDERS_FEATURE_GUIDE.md#Inventory-Management](ORDERS_FEATURE_GUIDE.md#inventory-management)
- **How do API calls work?** → See [ORDERS_API_REFERENCE.md#Implementation-Examples](ORDERS_API_REFERENCE.md#implementation-examples)

---

**Last Updated**: January 12, 2026  
**Status**: ✅ Complete & Production Ready  
**Maintained By**: Development Team
