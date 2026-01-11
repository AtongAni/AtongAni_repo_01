# Orders Feature - Customer UI Guide

## Overview

The **Orders View** component provides customers with a complete order history and real-time status tracking for all their purchases through the checkout staging system.

**Component**: `web/src/components/OrdersView.jsx`  
**Styling**: `web/src/components/OrdersView.css`

---

## User Interface Layout

### Header Section
```
┌─────────────────────────────────────────┐
│            My Orders                    │  ← Title
└─────────────────────────────────────────┘
```

### Order List View

#### Order Card (Collapsed View)
```
┌─────────────────────────────────────────────────────┐
│  Order #1234                        ⏳ IN_PROGRESS   │
│  Jan 12, 2026                                       │
│  Order Total: ₱650.00                              │
│  [Click to expand ▼]                                │
└─────────────────────────────────────────────────────┘
```

#### Order Card (Expanded View)
```
┌─────────────────────────────────────────────────────┐
│  Order #1234                  ⏳ IN_PROGRESS          │
│  Jan 12, 2026                                       │
│  Order Total: ₱650.00                              │
├─────────────────────────────────────────────────────┤
│  Order Items:                                       │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │ Tomatoes                                     │  │
│  │ From: Maria's Farm                           │  │
│  │ Quantity: 5 kg  Unit Price: ₱100            │  │
│  │ Subtotal: ₱500.00                           │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │ Corn                                         │  │
│  │ From: Green Valley Farm                      │  │
│  │ Quantity: 3 bundles  Unit Price: ₱50        │  │
│  │ Subtotal: ₱150.00                           │  │
│  └──────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────┤
│  Rejection Reason (if rejected):                    │
│  "Out of stock on fresh tomatoes"                   │
└─────────────────────────────────────────────────────┘
```

---

## Status Badges

### Visual Status Indicators

Four distinct order statuses with unique icons and colors:

#### 1. ⏳ IN_PROGRESS (Light Blue)
- **Icon**: Hourglass ⏳
- **Background Color**: Light blue (#E3F2FD)
- **Text Color**: Dark blue
- **Meaning**: Farmer is reviewing the order, awaiting approval or rejection
- **Duration**: Usually a few minutes to hours
- **Customer Action**: Wait for farmer response

#### 2. ✅ APPROVED (Green)
- **Icon**: Checkmark ✅
- **Background Color**: Light green (#E8F5E9)
- **Text Color**: Dark green
- **Meaning**: Farmer has accepted the order, inventory reduced
- **Next Step**: Order moving to fulfillment
- **Customer Action**: Order will be prepared/delivered

#### 3. ❌ REJECTED (Red)
- **Icon**: X mark ❌
- **Background Color**: Light red (#FFEBEE)
- **Text Color**: Dark red
- **Meaning**: Farmer declined the order
- **Reason Display**: Shows explanation below order details
- **Customer Action**: Items returned to cart, can retry with different farmer

#### 4. 🎉 COMPLETED (Gold/Yellow)
- **Icon**: Party/Celebration 🎉
- **Background Color**: Light yellow (#FFFDE7)
- **Text Color**: Dark orange
- **Meaning**: Order has been fulfilled
- **Final Status**: No further action needed
- **Customer Action**: None (order complete)

---

## Order Card Components

### Card Header Section
```
┌──────────────────────────────────────────┐
│  Order #1234                  ⏳ Status │  ← Order ID and Status Badge
│  Jan 12, 2026                           │  ← Order date (formatted)
│  Order Total: ₱650.00                   │  ← Total amount (2 decimals)
└──────────────────────────────────────────┘
```

**Fields**:
- **Order ID**: Unique identifier (e.g., #1234)
- **Status Badge**: Icon + status text in colored box
- **Date**: Formatted as locale-specific date (e.g., "1/12/2026")
- **Total Amount**: Currency symbol + amount with 2 decimal places

### Expandable Details Section

Click anywhere on the card to toggle expansion.

**When Expanded, Shows**:
1. **Order Items List**
   - Product name
   - Farmer/seller name ("From: ...")
   - Quantity and unit
   - Unit price
   - Subtotal (quantity × price)

2. **Rejection Reason** (only if status is REJECTED)
   - Farmer's explanation for rejection
   - Helps customer understand why order was declined

---

## Real-Time Updates

### Polling Mechanism
- **Interval**: Every 5 seconds
- **Trigger**: Page load + automatic background polling
- **Updates**: Fetches latest order data from backend
- **Refresh**: Order list and status badges update automatically

### Live Status Tracking
When farmer approves/rejects an order:
1. Status badge changes within 5 seconds
2. No manual refresh needed
3. Rejection reason appears if rejected
4. Customer sees real-time order progress

### No Manual Refresh Required
- Entire page stays responsive
- Automatic polling in background
- User can see changes happen live
- Updates are quiet (no annoying notifications)

---

## Empty State

When customer has no orders:
```
┌─────────────────────────────────────────┐
│        No orders yet                    │
│                                         │
│   You haven't placed any orders.       │
│   Start shopping to see them here!      │
│                                         │
│   [Continue Shopping Button]            │
└─────────────────────────────────────────┘
```

---

## Data Display Format

### Order Information
| Field | Format | Example |
|-------|--------|---------|
| Order ID | `Order #{id}` | `Order #1234` |
| Date | Locale-specific | `1/12/2026` |
| Total | `₱{amount}` with 2 decimals | `₱650.00` |
| Status | Icon + text | `⏳ IN_PROGRESS` |

### Item Information
| Field | Format | Example |
|-------|--------|---------|
| Product | Product title | `Tomatoes` |
| Farmer | "From: {name}" | `From: Maria's Farm` |
| Quantity | `{qty} {unit}` | `5 kg` |
| Unit Price | `₱{price}` | `₱100` |
| Subtotal | `₱{amount}` | `₱500.00` |

### Rejection Reason
- **Label**: "Rejection Reason (if rejected):"
- **Display**: Text provided by farmer
- **Visibility**: Only shows if order status is REJECTED
- **Length**: Can be multiple lines
- **Example**: "Out of stock on fresh tomatoes"

---

## Interaction Patterns

### Expanding Order Details
1. Click anywhere on the order card
2. Card expands smoothly (animation)
3. Item list becomes visible
4. Rejection reason shows (if applicable)
5. Click again to collapse

### Status Monitoring
1. Customer places order (status: IN_PROGRESS)
2. Waits for farmer response
3. Order status changes to APPROVED or REJECTED
4. Dashboard updates automatically within 5 seconds
5. Customer sees new status badge and reason (if rejected)

### Next Steps Based on Status
- **IN_PROGRESS**: "Your order is being reviewed"
- **APPROVED**: "Your order has been accepted!"
- **REJECTED**: "Items have been returned to your cart"
- **COMPLETED**: "Thank you for your order!"

---

## Mobile Responsiveness

### Responsive Breakpoints
- **Large Screens** (≥1024px):
  - Full-width order cards with generous padding
  - Expanded details visible inline
  - Date and status on same line

- **Tablet** (768px - 1023px):
  - Order cards adjusted for tablet width
  - Readable font sizes
  - Comfortable touch targets

- **Mobile** (< 768px):
  - Full-width cards with appropriate padding
  - Stacked layout for order details
  - Tap-friendly expansion (min 44px height)
  - Status badge wraps if needed
  - Touch-friendly item expansion

### Mobile Features
- Swipe to expand/collapse (optional)
- Large tap targets for interaction
- Text readable without scrolling
- Images/icons scale appropriately
- Dates are readable on small screens

---

## Color Scheme

```css
/* Status Badge Colors */
IN_PROGRESS: Light Blue (#E3F2FD) text, dark blue text
APPROVED: Light Green (#E8F5E9) text, dark green text
REJECTED: Light Red (#FFEBEE) text, dark red text
COMPLETED: Light Yellow (#FFFDE7) text, dark orange text

/* Card Styling */
Background: White (#FFFFFF)
Border: Light gray (#E0E0E0) or shadow
Hover: Subtle shadow increase
Active/Expanded: Slightly darker background

/* Text Colors */
Primary: Dark gray (#212121)
Secondary: Medium gray (#666666)
Light: Light gray (#CCCCCC)
```

---

## Keyboard Navigation

| Key | Action |
|-----|--------|
| `Tab` | Navigate between order cards |
| `Enter` | Expand/collapse focused order card |
| `Space` | Expand/collapse focused order card |
| `Escape` | Collapse expanded card |
| `Arrow Down` | Move to next order |
| `Arrow Up` | Move to previous order |

---

## Features Summary

✅ **Real-Time Status Tracking**
- See order progress as it happens
- Automatic updates every 5 seconds
- No manual refresh needed

✅ **Clear Status Indicators**
- Color-coded badges
- Icon indicators
- Easy-to-understand status text

✅ **Detailed Order Information**
- See all items in order
- Farmer names for each item
- Prices and subtotals
- Order total and date

✅ **Rejection Handling**
- See rejection reason if declined
- Items automatically returned to cart
- Can retry with different approach

✅ **Expandable Details**
- Clean collapsed view
- Click to see full details
- Smooth expansion animation

✅ **Mobile-Friendly**
- Works on all screen sizes
- Touch-friendly interactions
- Readable on small screens

---

## Common Use Cases

### Scenario 1: Placing an Order
1. Customer adds items to cart
2. Clicks "Checkout"
3. Gets order confirmation
4. Navigates to "My Orders"
5. Sees order with ⏳ IN_PROGRESS status
6. Waits for farmer decision

### Scenario 2: Order Approved
1. Customer checks orders periodically
2. Dashboard auto-updates every 5 seconds
3. Status changes to ✅ APPROVED
4. Customer receives confirmation
5. Order proceeds to fulfillment

### Scenario 3: Order Rejected
1. Customer checking order history
2. Status shows ❌ REJECTED
3. Rejection reason visible below order
4. Items automatically in cart again
5. Customer can retry checkout

### Scenario 4: Monitoring Multiple Orders
1. Customer has 3 active orders
2. Each shows different status
3. Updates happen in real-time
4. Can track all orders simultaneously
5. Manage from single dashboard

---

## Error Handling

### Network Errors
- **If polling fails**: Continues retrying silently
- **If order expansion fails**: Shows error message
- **Recovery**: Automatic retry on next poll interval

### Data Display Errors
- **Missing prices**: Defaults to ₱0.00
- **Invalid dates**: Shows timestamp instead
- **Missing farmer name**: Shows "From: Unknown"

### User Feedback
- Success messages on actions
- Error messages with context
- Retry options when available
- Clear explanations of issues

---

## Accessibility Features

- **Semantic HTML**: Proper heading structure
- **Color + Icons**: Status not conveyed by color alone
- **Keyboard Support**: Full keyboard navigation
- **Screen Readers**: Proper ARIA labels
- **Focus States**: Visible focus indicators
- **Text Contrast**: Meets WCAG AA standards
- **Readable Fonts**: Sans-serif, appropriate sizing

---

## Performance Considerations

- **Polling Interval**: 5 seconds balances responsiveness and efficiency
- **Data Optimization**: Only fetches customer's orders
- **Rendering**: React efficiently updates changed orders
- **Network**: Minimal payload for polling requests
- **Memory**: Cached order data prevents redundant loads
- **CPU**: Smooth animations and transitions

---

**Last Updated**: January 12, 2026  
**Version**: 1.0  
**Status**: ✅ Complete & Production Ready
